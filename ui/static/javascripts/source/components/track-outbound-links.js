var $ = require('component-dom');

module.exports = {
    init: function () {

        var $body = $('body');

        $body.on('click', 'a', function ( e ) {
            var url = e.target.href;
            if ( /\/tickets/.test(window.location.href) ) {
                e.preventDefault();
                ga('send', 'event', 'outbound', 'click', url, {'hitCallback': function () {
                    document.location = url;
                }});
            }
        });

    }
};
