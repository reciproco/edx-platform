# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_groups', '0001_initial'),
        ('bulk_email', '0002_data__load_course_email_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_type', models.CharField(default=b'myself', max_length=64, choices=[(b'myself', b'Myself'), (b'staff', b'Staff and instructors'), (b'learners', b'All students'), (b'cohort', b'Send to a specific cohort'), (b'all', b'All')])),
            ],
        ),
        migrations.AlterField(
            model_name='courseemail',
            name='to_option',
            field=models.CharField(default=b'myself', max_length=64, choices=[(b'myself', b'Myself'), (b'staff', b'Staff and instructors'), (b'learners', b'All students'), (b'cohort', b'Send to a specific cohort'), (b'all', b'All')]),
        ),
        migrations.CreateModel(
            name='CohortTarget',
            fields=[
                ('target_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulk_email.Target')),
                ('cohort', models.ForeignKey(to='course_groups.CourseUserGroup')),
            ],
            bases=('bulk_email.target',),
        ),
        migrations.CreateModel(
            name='AllTarget',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('bulk_email.target',),
        ),
        migrations.CreateModel(
            name='LearnersTarget',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('bulk_email.target',),
        ),
        migrations.CreateModel(
            name='MyselfTarget',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('bulk_email.target',),
        ),
        migrations.CreateModel(
            name='StaffTarget',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('bulk_email.target',),
        ),
        migrations.AddField(
            model_name='courseemail',
            name='targets',
            field=models.ManyToManyField(to='bulk_email.Target'),
        ),
    ]
