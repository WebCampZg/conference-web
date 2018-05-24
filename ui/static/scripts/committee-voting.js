$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' && !this.crossDomain) {
            var csrfToken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookiesokie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function rateApplication(applicationID, score) {
    var url = "/dashboard/applications/rate/";

    var data = {
        "application_id": applicationID,
        "score": score,
    }

    $.post(url, data)
        .done(function(data) {
            var $application = $('.application[data-application-id="' + applicationID + '"]');
            $application.find('button[data-score]').addClass('hollow');
            $application.find('button[data-score="' +  score +'"]').removeClass('hollow')
        });
}

function unrateApplication(applicationID) {
    var url = "/dashboard/applications/unrate/";

    var data = {
        "application_id": applicationID,
    }

    $.post(url, data)
        .done(function(data) {
            var $application = $('.application[data-application-id="' + applicationID + '"]');
            $application.find('button[data-score]').addClass('hollow');
        });
}

$(document).ready(function () {
    $("[data-rate-application]").click(function() {
        var applicationID = $(this).data('application-id');
        var score = $(this).data('score');

        rateApplication(applicationID, score);
    });

    $("[data-unrate-application]").click(function() {
        var applicationID = $(this).data('application-id');

        unrateApplication(applicationID);
    });
});

$(document).keypress(function(e) {
    if (e.ctrlKey || e.shiftKey || e.altKey || e.metaKey) {
        return
    }

    switch(e.which) {
        case 48: // 0
            e.preventDefault();
            $("[data-unrate-application]").click();
            break;

        case 49: // 1
        case 50: // 2
        case 51: // 3
        case 52: // 4
        case 53: // 5
            var score = e.which - 48;
            e.preventDefault();
            $("[data-rate-application][data-score='" + score + "']").click();
            break;
    }
});