var $ = require('component-dom');

module.exports = {
    init: function () {

        $el = $('.js-sharePopup');

        $el.on('click', function ( e ) {

            var $link = $(e.currentTarget);

            e.preventDefault();

            open(
                $link.attr('href'),
                'sharePopup',
                'width=600,height=600,top=100,left=100,menubar=no,scrollbars=no,status=no,toolbar=no'
            );

        });

    }
};
