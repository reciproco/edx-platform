# pylint: disable=missing-docstring
import logging

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Q
from opaque_keys.edx.keys import CourseKey
from provider.oauth2.models import Client

from certificates.models import GeneratedCertificate
from openedx.core.djangoapps.programs.models import ProgramsApiConfig
from openedx.core.djangoapps.programs.tasks.v1.tasks import award_program_certificates
from openedx.core.djangoapps.programs.utils import get_programs


# TODO: Log to console, even without debug enabled?
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Backpopulate missing program credentials.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c', '--commit',
            action='store_true',
            dest='commit',
            default=False,
            help='Submit tasks for processing.'
        )

    def _flatten(self, programs):
        """Flatten program dicts into a list of run modes."""
        run_modes = []
        for program in programs:
            for course_code in program['course_codes']:
                for run in course_code['run_modes']:
                    run_modes.append(
                        # TODO: Named tuple
                        (CourseKey.from_string(run['course_key']), run['mode_slug'])
                    )

        return run_modes

    def handle(self, *args, **options):
        commit = options.get('commit')

        programs_config = ProgramsApiConfig.current()
        client = Client.objects.get(name=programs_config.OAUTH2_CLIENT_NAME)

        if client.user is None:
            msg = (
                'No user is associated with the %s OAuth2 client. No tasks have been enqueued. '
                'Associate a user with the client and try again.'
            ).format(programs_config.OAUTH2_CLIENT_NAME)

            logger.error(msg)
            return

        programs = get_programs(client.user)
        run_modes = self._flatten(programs)

        logger.info('Querying for users who may be eligible for a program certificate.')

        query = reduce(lambda x, y: x | y, [Q(course_id=r[0], mode=r[1]) for r in run_modes])
        username_dicts = GeneratedCertificate.eligible_certificates.filter(query).values('user__username').distinct()
        usernames = [d['user__username'] for d in username_dicts]

        if commit:
            logger.info('Enqueuing tasks for %d eligible users.', len(usernames))
        else:
            logger.info(
                'Found %d eligible users. To enqueue tasks, pass the -c or --commit flags.',
                len(usernames)
            )
            return

        # TODO: Slow-start for congestion control?
        succeeded, failed = 0, 0
        for username in usernames:
            try:
                award_program_certificates.delay(username)
            except:  # pylint: disable=bare-except
                failed += 1
                logger.exception('Failed to enqueue program certification task for user [%s]', username)
            else:
                succeeded += 1
                logger.info('Successfully enqueued task for user [%s]', username)

        logger.info('Done. %d succeeded. %d failed.', succeeded, failed)
