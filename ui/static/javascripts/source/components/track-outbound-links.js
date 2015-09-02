var $ = require('component-dom');

module.exports = {
    init: function () {

        var $a = $('a');

        $a.on('click', function ( e ) {
            var url = e.currentTarget.href;
            if ( /entrio\.hr/.test(url) ) {
                console.log(1);
                e.preventDefault();
                ga('send', 'event', 'outbound', 'click', url, {'hitCallback': function () {
                    document.location = url;
                }});
            }
        });

    }
};
