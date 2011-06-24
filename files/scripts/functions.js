// functions.js : main JS functions for my app.

var loading = "<div class='loading'>جاري التحميل</div>";

function fb_exit() {
    top.location.href = 'http://www.facebook.com/home.php';
}

function get_menu(path, fb_id) {
    $("rightPageContent").html(loading)
    
    $.post(path+'/menu/', {fb_user_id: fb_id}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    }).error(function() {get_menu(path, fb_id)});
}

function get_about(path) {
    $("#leftPage").html(loading);
    
    $.post(path+'/about/', function(d) {
        $("#leftPage").hide();
        $("#leftPage").fadeIn(1000);
        $("#leftPage").html(d);
    }).error(function() {get_about(path)});
}

function get_statistics(path, fb_id) {

    $("#leftPage").html(loading);
    
    $.post(path+'/statistics/', {fb_user_id: fb_id}, function(d) {
        $("#leftPage").hide();
        $("#leftPage").fadeIn(1000);
        $("#leftPage").html(d);
    }).error(function() {get_statistics(path, fb_id)});
}

function get_rounds(path, fb_id) {
    $("rightPageContent").html(loading)
    
    $.post(path+'/rounds/', {fb_user_id: fb_id}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    }).error(function() {get_rounds(path, fb_id)});
}

function submit_new_round(path, fb_id) {
    var parts_num = $("#parts_num").attr('value');
    var radio = $("#directionASC").attr('checked');
    var direction;
    if (radio == 'checked') {
        direction = 'asc';
    }
    else {
        direction = 'desc';
    };
    if (parts_num < 2 && direction == 'asc') {
        alert("خطأ! لا يُمكن إختيار أقل من 3 أجزاء في الإتجاه التصاعدي.");
        return false;
    };
    $.post(path+'/rounds/', {fb_user_id: fb_id, parts_num: parts_num, direction: direction}, function(d) {
        $("#rightPageContent").hide().fadeIn(1000).html(d);
    }).error(function() {submit_new_round(path, fb_id);});
    return false;
}

var TotalSeconds =  35;
var t;
var f;

function get_random_aya(path, round_id) {
    $("#aya").css("visiblity", "hidden");
    $("#Loading_Question").show();
    f = setTimeout('checkAya("'+path+'",'+round_id+');', 5000);
    $.getJSON(path+'/json/get_random_aya/', {roundId: round_id}, function(d, status, xhr) {
        $("#Loading_Question").hide();
        $("#error_waiting").hide();
        $("#aya").fadeIn(1000).html(d.ayaOthmani);
        $("#ayaId").attr('value', d.ayaId);
        $("#submit").attr("disabled", false).removeClass("disabled");
        TotalSeconds = 35;
        t = CreateTimer(path, round_id);
    }).error(function() {get_random_aya(path, round_id);});
}

function get_round_statistics(path, round_id) {
    $.get(path+'/statistics/', {round_id: round_id}, function(d) {
        $("#leftPage").html(d);
    });
}

var ti;

function CreateTimer(path, round_id) {
    
    $("#timerNum").html(TotalSeconds);
    $("#timer").show();
    if (TotalSeconds <= 0) {
        $("#timer").hide();
        get_random_aya(path, round_id);
        return;
    }
    
    if (TotalSeconds == 'S') {
        return;
    }

    TotalSeconds -= 1;
    $("#timerNum").html(TotalSeconds);
    $("#timer").show();
    ti = setTimeout("CreateTimer('"+path+"',"+round_id+")", 1000);
}

function pausecomp(millis)
 {
  var date = new Date();
  var curDate = null;
  do { curDate = new Date(); }
  while(curDate-date < millis);
}

function stopTimer() {
    TotalSeconds = 'S';
    pausecomp(1010);
    clearTimeout(ti);
}

function checkAya(path, round_id) {
    if (TotalSeconds != 'S' || TotalSeconds > 0) {
        clearTimeout(f);
        return;
    };
    $("#error_waiting").show();
}

function submit_answer(path, round_id, fb_id) {
    stopTimer();
    $("#submit").attr("disabled", true).addClass("disabled");
    var ayaId = $("#ayaId").attr('value')
    var sura = $("#sura").attr('value')
    $.getJSON(path+'/json/validate_aya/', {roundId: round_id, ayaId: ayaId, sura: sura}, function(d) {
        if (d.result == true) {
            $("#resultFail").hide();
            $("#resultSuccess").fadeIn(1000);
            if (d.is_finished) {
                // get_menu(path, fb_id);
		// get_statistics(path, fb_id);
		window.location.href = path+"/";
            }
            else {
                $("#timer").hide();
                get_random_aya(path, round_id);
            }
            setTimeout('$("#resultSuccess").fadeOut(1000);', 3000);
        }
        else {
            $("#resultSuccess").hide();
            $("#timer").hide();
            $("#resultFail #sura_correct").html(d.correctSura);
            $("#resultFail").fadeIn(1000);
            get_random_aya(path, round_id);
            setTimeout('$("#resultFail").fadeOut(1000);', 3000);
        }
        $("#statistics").hide();
        $("#statistics #question_num").html(d.question_num);
        $("#statistics #correct_answers").html(d.correct_answers);
        $("#statistics #wrong_answers").html(d.wrong_answers);
        $("#statistics #points").html(d.points);
        $("#statistics").fadeIn(1000);
        $("#sura").attr('value','').focus();
    }).error(function() {submit_answer(path, round_id, fb_id);});
    return false;
}

function cancel_round(path, round_id, fb_id) {
	c = confirm('هل أنت متأكد؟ لن يتم حساب النقاط التي حصلت عليها!')
    if (c == true) {
		$.getJSON(path+'/json/cancel_round/', {roundId: round_id}, function(d) {
			if (d.result == true) {
                stopTimer();
				get_menu(path, fb_id);
				get_statistics(path, fb_id);
			};
		});
	}
}