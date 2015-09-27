var $ = require('component-dom');

module.exports = {
    init: function () {

        var $nav = $('.Schedule-nav');

        if ( !$nav.length ) {
            return;
        }

        var $table = $('.Schedule-table');
        var $link = $('.Schedule-navLink');

        $nav.on('click', '.Schedule-navLink', function ( e ) {

            e.preventDefault();

            var $el = $(e.delegateTarget);

            $link.removeClass('Button--alpha');
            $link.addClass('Button--gamma');
            $el.removeClass('Button--gamma');
            $el.addClass('Button--alpha');
            $table.addClass('is-hidden');
            $('#' + $el.attr('data-block')).removeClass('is-hidden');

        });

    }
};
