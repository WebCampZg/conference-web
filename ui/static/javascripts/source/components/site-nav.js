var $ = require('component-dom');

module.exports = {

    init: function () {

        this.$el = $('.SiteNav');
        this.$html = $('html');

        this.setupEvents();

    },

    setupEvents: function () {

        this.$el.on('click', '.SiteNav-toggler', function ( e ) {

            e.preventDefault();

        }.bind(this));

        this.$el.on('click', '.SiteNav-toggler--open', this.open.bind(this));
        this.$el.on('click', '.SiteNav-toggler--close', this.close.bind(this));

    },

    open: function () {

        this.$html.addClass('is-siteNavOpened');
        this.$el.addClass('is-opened');

    },

    close: function () {

        this.$html.removeClass('is-siteNavOpened');
        this.$el.removeClass('is-opened');

    }

};
