;(function (define, undefined) {
    'use strict';
    define([
        'gettext',
        'jquery',
        'underscore',
        'backbone',
        'js/student_account/views/account_section_view',
        'text!templates/student_account/account_settings.underscore'
    ], function (gettext, $, _, Backbone, AccountSectionView, accountSettingsTemplate) {

        var AccountSettingsView = Backbone.View.extend({

            navLink: '.account-nav-link',
            activeTab: 'about_sections',
            AccountSettingsTabs: [
                    {name: 'about_sections', label: gettext('About'), class: 'active'},
                    {name: 'connected_account_sections', label: gettext('Connected Accounts')}
            ],
            events: {
                'click .account-nav-link': 'changeTab'
            },

            initialize: function (options) {
                this.options = _.extend({}, options);
                this.sections = {
                    about_sections: this.options.aboutSectionsData,
                    connected_account_sections: this.options.accountsSectionData
                };
                _.bindAll(this, 'render', 'changeTab', 'showLoadingError');
            },

            render: function () {
                this.$el.html(_.template(accountSettingsTemplate)({
                    accountSettingsTabs: this.AccountSettingsTabs
                }));
                this.renderSection(this.sections[this.activeTab]);
                return this;
            },

            changeTab: function(e) {
                e.preventDefault();
                var $currentTab = $(e.target);
                this.activeTab = $currentTab.data('name');
                this.renderSection(this.sections[this.activeTab]);

                $(this.navLink).removeClass("active");
                $currentTab.addClass("active");
            },

            renderSection: function (sections) {
                var accountSectionView = new AccountSectionView({
                    sections: sections,
                    el: '.account-settings-sections'
                });

                accountSectionView.render();
                accountSectionView.renderFields();
            },

            showLoadingError: function () {
                this.$('.ui-loading-indicator').addClass('is-hidden');
                this.$('.ui-loading-error').removeClass('is-hidden');
            }
        });

        return AccountSettingsView;
    });
}).call(this, define || RequireJS.define);
