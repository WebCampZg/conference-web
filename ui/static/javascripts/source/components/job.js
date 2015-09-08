var $ = require('component-dom');

module.exports = {
    init: function () {

        var $container = $('.Job');

        if ( !$container.length ) {
            return;
        }

        var $body = $('.Job-body');

        $body.addClass('is-hidden');

        $container.on('click', '.Job-readMore', function ( e ) {
            var $el = $(e.delegateTarget);
            var $filteredBody = $body.filter(function ( el ) {
                return $(el).attr('data-job-slug') === $el.attr('data-job-slug');
            });

            if ( $filteredBody.hasClass('is-hidden') ) {
                $el.addClass('is-active');
                $filteredBody.removeClass('is-hidden');
            } else {
                $el.removeClass('is-active');
                $filteredBody.addClass('is-hidden');
            }

        });

    }
};
