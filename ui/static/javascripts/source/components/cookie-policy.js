var $ = require('component-dom');
var raf = require('component-raf');
var cookie = require('cookie-monster');
var html = require('fs').readFileSync('ui/templates/partials/cookie-policy.html', 'utf8');

module.exports = {
    init: function () {

        var $el;

        if ( cookie.get('wczgCookiePolicyAgreement') ) {
            return;
        }

        $('body').prepend(html);

        $el = $('.CookiePolicy');

        raf(function () {
            $el.addClass('is-visible');
        });

        $el.on('click', '.Button', function () {

            cookie.set('wczgCookiePolicyAgreement', 1, {
                expires: new Date(2042, 0)
            });

            $el.addClass('is-agreed');

        });

    }
};
