<!-- Content -->
%include honor_board 
<div id="content" class="content">
    <script type="text/javascript">
        FB.Canvas.setSize({ width: 760, height: 600 }); // Live in the past
    </script>
    <script type="text/javascript">
        $(document).ready(function() {
            get_menu('{{rq.script}}','{{user.fb_id}}');
            get_statistics('{{rq.script}}', '{{user.fb_id}}');
        });
    </script>
    <div id="rightPage" class="rightPage">
        <h1><img src="{{rq.script}}/images/logo.png" alt="مسابقة لآلئ الفرقان" id="logo" width="250" /></h1>
        <h3>مرحبًا بك <a href="http://www.facebook.com/profile.php?id={{user.fb_id}}" title="الملف الشخصي">{{user.fb_full_name}}</a></h3>
        <div id="rightPageContent">
            <div class="loading">جاري التحميل</div>
        </div><!-- #rightPageContent -->
        <embed class="hidden" src="{rq.script}}/audios/_quran_nasheed.mp3" autostart="true" />
        <audio autoplay="autoplay" loop="loop">
          <source src="{{rq.script}}/audios/quran_nasheed.ogg" type="audio/ogg" />
          <source src="{{rq.script}}/audios/_quran_nasheed.mp3" type="audio/mpeg" />
        Your browser does not support the audio element.
        </audio> 
    </div><!-- rightPage -->
    <div id="leftPage" class="leftPage">
        <div class="loading">جاري التحميل</div>
    </div><!-- #leftPage -->
</div><!-- #content -->
%include extra_points rq=rq, user=user
