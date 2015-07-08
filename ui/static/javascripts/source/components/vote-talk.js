var $ = require('component-dom');

module.exports = {
    init: function () {

        var $voteTalk = $('.VoteTalk');

        if ( !$voteTalk.length ) {
            return;
        }

        var $voteTalkBody = $('.VoteTalk-body');

        $voteTalkBody.addClass('is-hidden');

        $voteTalk.on('click', '.VoteTalk-readMore', function ( e ) {

            var $el = $(e.delegateTarget);
            var $body = $voteTalkBody.filter(function ( el ) {
                return $(el).attr('data-talk-slug') === $el.attr('data-talk-slug');
            });

            if ( $body.hasClass('is-hidden') ) {
                $el.addClass('is-active');
                $body.removeClass('is-hidden');
            } else {
                $el.removeClass('is-active');
                $body.addClass('is-hidden');
            }

        });

    }
};
