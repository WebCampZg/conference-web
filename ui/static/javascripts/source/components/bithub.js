var $ = require('component-dom');
var inViewport = require('component-in-viewport');
var debounce = require('debounce');

module.exports = {
    init: function () {

        var $bithub = $('.Bithub');

        if ( !$bithub.length ) {
            return;
        }

        var $script = $bithub.find('script');

        window.addEventListener('scroll', debounce(function () {
            if ( inViewport($bithub[0], 100) && !$script.attr('src') ) {
                $script.attr('src', $script.attr('data-src'));
            }
        }, 300));

    }
};
