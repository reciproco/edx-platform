;(function (define, undefined) {
    'use strict';
    define([
        'gettext',
        'jquery',
        'underscore',
        'backbone',
        'text!templates/student_account/account_settings_section.underscore'
    ], function (gettext, $, _, Backbone, sectionTemplate) {

        var AccountSectionView = Backbone.View.extend({

            initialize: function (options) {
                this.options = _.extend({}, options);
                _.bindAll(this, 'render', 'renderFields');
            },

            render: function () {
                this.$el.html(_.template(sectionTemplate)({
                    sections: this.options.sections
                }));
            },

            renderFields: function () {
                var view = this;
                view.$('.ui-loading-indicator').addClass('is-hidden');

                _.each(view.$('.account-settings-section-body'), function (sectionEl, index) {
                    _.each(view.options.sections[index].fields, function (field) {
                        $(sectionEl).append(field.view.render().el);
                    });
                });
                return this;
            }
        });

        return AccountSectionView;
    });
}).call(this, define || RequireJS.define);
