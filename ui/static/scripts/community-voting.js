function success(button, voted) {
    if (voted) {
        button.removeClass("hollow").addClass("yellow").addClass("voted").removeClass("not-voted");
        button.data("voted", true);
    } else {
        button.addClass("hollow").removeClass("yellow").removeClass("voted").addClass("not-voted");
        button.data("voted", false);
    }
}

function failure(error)
{
    var text = "Action failed.\nError: " + error + "\nContact the admin at info@webcampzg.org";
    alert(text);
}

$(document).ready(function () {
    $("[data-vote-button]").on('click', function(e) {
        var button = $(e.target);
        var talkID = button.data('talk-id');
        var ticketCode = button.data('ticket-code');
        var voted = button.data('voted');
        var action = voted ? 'rm': 'add';
        var url = '/voting/' + ticketCode + '/vote/' + action + '/' + talkID + '/';

        $.post(url)
            .done(function(data) {
                if (data.error) {
                    failure(data.error);
                } else {
                    success(button, data.voted);
                }
            })
            .fail(function (jqXHR, textStatus, errorThrown) {
                failure(errorThrown);
            })
    });
});
