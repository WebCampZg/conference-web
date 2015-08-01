var $ = require('component-dom');
var jQuery = require('jquery');

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


        var $voteTalkButton = $('.VoteTalk-action');

        jQuery(document).ready(function(){
            $voteTalkButton.each(function(el){
                if (el.attr('data-voted') == 'True'){
                    el.prop('checked', true);
                }
            });
        });

        $voteTalkButton.on('click', function(e){
            var checked = $(this).prop('checked');

            var action = null;
            if (checked){
                action = 'add'
            }
            else{
                action = 'rm'
            }
            var url = '/voting/vote/' + action + '/' + $(this).attr('data-talk-id') + '/';
            jQuery.post(url, function(data){
                if(data['error']){
                    console.log('Handle error: ' + data['error']);
                }
                else{
                    console.log('Cool: ' + data['message']);
                }
            }).fail(function(data){
               console.log('Handle other error: ' + data['status'] + ' ' + data['statusText']);
            });

        });

    }
};
