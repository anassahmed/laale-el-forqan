// functions.js : main JS functions for my app.

var loading = "<div class='loading'>جاري التحميل</div>";

function fb_exit() {
    top.location.href = 'http://www.facebook.com/home.php';
}

function get_menu(path, fb_id) {
    $("rightPageContent").html(loading)
    
    $.post(path+'/menu/', {fb_user_id: fb_id}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    });
}

function get_about(path) {
    $("#leftPage").html(loading);
    
    $.post(path+'/about/', function(d) {
        $("#leftPage").hide();
        $("#leftPage").fadeIn(1000);
        $("#leftPage").html(d);
    });
}

function get_statistics(path, fb_id) {

    $("#leftPage").html(loading);
    
    $.post(path+'/statistics/', {fb_user_id: fb_id}, function(d) {
        $("#leftPage").hide();
        $("#leftPage").fadeIn(1000);
        $("#leftPage").html(d);
    });
}

function get_rounds(path, fb_id) {
    $("rightPageContent").html(loading)
    
    $.post(path+'/rounds/', {fb_user_id: fb_id}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    });
}

function submit_new_round(path, fb_id) {
    var parts_num = $("#parts_num").attr('value');
    var radio = $("#directionASC").attr('checked');
    var direction;
    if (radio == true) {
        direction = 'asc';
    }
    else {
        direction = 'desc';
    }
    $.post(path+'/rounds/', {fb_user_id: fb_id, parts_num: parts_num, direction: direction}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    });
    return false;
}

function get_random_aya(path, round_id) {
    $("#aya").hide();
    $.getJSON(path+'/json/get_random_aya/', {roundId: round_id}, function(d) {
        $("#aya").hide().fadeIn(1000).html(d.ayaOthmani);
        $("#ayaId").attr('value', d.ayaId);
    });
}

function get_round_statistics(path, round_id) {
    $.get(path+'/statistics/', {round_id: round_id}, function(d) {
        $("#leftPage").html(d);
    });
}

function submit_answer(path, round_id, fb_id) {
    var ayaId = $("#ayaId").attr('value')
    var sura = $("#sura").attr('value')
    $.getJSON(path+'/json/validate_aya/', {roundId: round_id, ayaId: ayaId, sura: sura}, function(d) {
        if (d.result == true) {
            $("#resultFail").hide();
            $("#resultSuccess").fadeIn(1000);
            if (d.is_finished) {
                window.location.href = 'http://apps.facebook.com/quran-quize/';
            }
            else {
                get_random_aya(path, round_id)
            }
            setTimeout('$("#resultSuccess").fadeOut(1000);', 5000);
        }
        else {
            $("#resultSuccess").hide();
            $("#resultFail #sura_correct").html(d.correctSura);
            $("#resultFail").fadeIn(1000);
            get_random_aya(path, round_id)
            setTimeout('$("#resultFail").fadeOut(1000);', 5000);
        }
        $("#statistics").hide();
        $("#statistics #question_num").html(d.question_num);
        $("#statistics #correct_answers").html(d.correct_answers);
        $("#statistics #wrong_answers").html(d.wrong_answers);
        $("#statistics #points").html(d.points);
        $("#statistics").fadeIn(1000);
        $("#sura").attr('value','').focus();
    });
    return false;
}

function like() {
    var likeCode = document.getElementById('likeBox').innerHTML;
    jAlert(likeCode);
}
