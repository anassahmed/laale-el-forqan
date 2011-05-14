<!-- Extra Points -->

<div id="extraPoints" class="extraPoints">
    <div class="like">
        <div id="fb-root"></div>
        <script src="http://connect.facebook.net/ar_AR/all.js#appId=211500928874964&amp;xfbml=1"></script>
        <fb:like href="http://apps.facebook.com/quran-quize/" send="false" width="450" height="100" show_faces="true" font=""></fb:like>
    </div><!-- .like -->
    
    <div class="bookmark">
        <fb:bookmark></fb:bookmark>
    </div><!-- .bookmark -->
    
    <br />
    
    <div class="invite">

        <button id="invite">
            ادع أصدقاءك!
            <br />
            <span style="color: yellow;">+100</span>
        </a>

    </div><!-- .invite -->
    
    <div id="fb-root"></div>
    
    <script>
        window.fbAsyncInit = function() {
            FB.init({
              appId   : '211500928874964',
              status  : true,
              cookie  : true,
              xfbml   : true
            });
        };
     
        $('#invite').click(sendRequest);
        function sendRequest() {
            FB.ui({
                method: 'apprequests',
                message: 'شاركوا معي في هذا المسابقة واختبركوا قوة حفظكم!',
                title: 'ادعُ أصدقائك لمسابقة لآلئ القرآن',
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
     
        (function() {
        var e = document.createElement('script');
        e.src = document.location.protocol + '//connect.facebook.net/ar_AR/all.js';
        e.async = true;
        document.getElementById('fb-root').appendChild(e);
        }());
    </script>

</div>
