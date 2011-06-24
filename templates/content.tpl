<!-- Content -->

<!-- Honor Board -->

<div id="honorBoard" class="honorBoard">
    <h3> لوحة الشرف </h3>
	%rank = 0
	%for i in heroes:
	    %rank += 1
	    %if len(i.user.fb_full_name) > 17:
			%full_name = i.user.fb_full_name[:15] + u'...'
		%else:
			%full_name = i.user.fb_full_name
		%end
		<div id="hero" class="hero">
			<a href="http://www.facebook.com/profile.php?id={{i.user.fb_id}}" target="_blank" title="الملف الشخصي"><img src="http://graph.facebook.com/{{i.user.fb_id}}/picture/" />{{full_name}}</a>
			<p>المرتبة: {{rank}}</p>
			<p>النقاط: {{i.total_points}}</p>
			
		</div>
    %end
</div>

<!-- real Content -->

<div id="content" class="content">
    <script type="text/javascript">
        window.fbAsyncInit = function() {
            FB.Canvas.setSize({ width: 760, height: 900 }); // Live in the past
        }
    </script>
    <script type="text/javascript">
        $(document).ready(function() {
            get_menu('{{rq.script}}','{{user.fb_id}}');
            get_statistics('{{rq.script}}', '{{user.fb_id}}');
            $("#soundButton").click(function() {
                if ($(this).hasClass('enabled')) {
                    document.getElementById('nasheed').pause();
                    $("#soundButton img").attr('src','{{rq.script}}/images/no_sound.png');
                    $(this).removeClass('enabled').addClass('disabled');
                }
                else {
                    document.getElementById('nasheed').play();
                    $("#soundButton img").attr('src','{{rq.script}}/images/sound.png');
                    $(this).removeClass('disabled').addClass('enabled');
                };
            });
        });
    </script>
    <div id="rightPage" class="rightPage">
        <h1><img src="{{rq.script}}/images/logo.png" alt="مسابقة لآلئ الفرقان" id="logo" width="250" /></h1>
        <h3>مرحبًا بك <a href="http://www.facebook.com/profile.php?id={{user.fb_id}}" target="_blank" title="الملف الشخصي">{{user.fb_full_name}}</a>
            <a id="soundButton" href="javascript: void(0)" class="enabled" title="تشغيل/كتم الصوت"><img style="width: 16px; height: 16px; float: left; margin-left: 10px;" src="{{rq.script}}/images/sound.png" /></a>        
        </h3>
        <div id="rightPageContent">
            <div class="loading">جاري التحميل</div>
        </div><!-- #rightPageContent -->
        <audio id="nasheed" autoplay="autoplay" loop="loop">
          <source src="{{rq.script}}/audios/quran_nasheed.ogg" type="audio/ogg" />
          <source src="{{rq.script}}/audios/_quran_nasheed.mp3" type="audio/mpeg" />
            <embed class="hidden" src="{{rq.script}}/audios/_quran_nasheed.mp3" autostart="true" />
        </audio> 
    </div><!-- rightPage -->
    <div id="leftPage" class="leftPage">
        <div class="loading">جاري التحميل</div>
    </div><!-- #leftPage -->
</div><!-- #content -->

<div id="free-open-source" class="note">
    <p><strong>مسابقة لآلئ الفرقان</strong> برمجية حُرة مفتوحة المصدر، يمكنك الإطلاع على مصدرها <a href="https://bitbucket.org/AnassAhmed/laale-el-forqan/">هنــــا</a></p>
</div><!-- #free-open-source -->

<!-- Extra Points -->

<div id="extraPoints" class="extraPoints">
    <div class="like">
        <div id="fb-root"></div>
        <script src="http://connect.facebook.net/ar_AR/all.js#appId=211500928874964&amp;xfbml=1"></script>
        <fb:like  href="http://www.facebook.com/apps/application.php?id=211500928874964" send="false" layout="standard" width="450" show_faces="true" font=""></fb:like>
    </div><!-- .like -->
    
    <div class="tools">

        <button id="invite" title="ادع أصدقائك، واربح 100 نقطة إضافية!">
            ادع أصدقاءك!
        </button>
        <button id="sendStatus" onClick="sendStatus();" title="أرسل مشاركة لنشر التطبيق!">
            أرسل مشاركة!
        </button>

    </div><!-- .invite -->
    
    <div id="fb-root"></div>
    
    <script>
        $('#invite').click(sendRequest);
        $('#sendStauts').click(sendStatus);
        function sendRequest() {
            FB.ui({
                method: 'apprequests',
                message: 'شاركوا معي في هذا المسابقة واختبروا قوة حفظكم!',
                title: 'ادعُ أصدقائك لمسابقة لآلئ القرآن!',
            },
            function (response) {
                if (response && response.request_ids) {
                    var requests = response.request_ids.join(',');
                    $.post('{{rq.script}}/invite/',{fb_user_id: {{user.fb_id}}, request_ids: requests},function(resp) {
                        if (resp) {
                            alert('تم دعوة الأصدقاء!');
                        }
                    });
                } else {
                    alert('تم الإلغاء!');
                }
            });
            return false;
        }

        function sendStatus() {
            FB.ui({ method: 'feed', 
                name: 'مسابقة لآلئ الفرقان',
                link: 'http://apps.facebook.com/quran-quize/',
                picture: 'http://www.darelnadwa.com/quran/images/Othman-128.png',
                caption: 'تطبيق فيسبوك',
                description: 'هذا التطبيق عبارة عن فكرة استلهمتُها من مسابقة خُضتها مع زملائي ونحن نراجع القرآن الكريم ليلة الإختبار، وكنا نفتح المصاحف بشكل عشوائي، والآية اللتي تقع عليها أعيننا، نسأل بعضنا عن السورة التي وردت فيها. وقد أعجبتني الفكرة ففكرت بتحويلها إلى تطبيق فيس بوك، يستفيد منه الكثير من الناس. ',
                message: 'اشتركوا في مسابقة لآلئ الفرقان، إنها مسابقة رائعة :)'});
            return false;
        }
     
        (function() {
        var e = document.createElement('script');
        e.src = document.location.protocol + '//connect.facebook.net/ar_AR/all.js';
        e.async = true;
        document.getElementById('fb-root').appendChild(e);
        }());
    </script>

</div>
