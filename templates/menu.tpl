<!-- Menu -->

%from functions import *

%if rq.q.has_key('fb_user_id'):
    %user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
%else:
    %raise forbiddenExeption()
%end

<div id="menu">
    <button id="start" onClick="get_rounds('{{rq.script}}', {{user.fb_id}});">إبدأ</button><br /><br />
    <button id="statistics" onClick="get_statistics('{{rq.script}}', {{user.fb_id}});">الإحصائيات</button><br /><br />
    <button id="about" onClick="get_about('{{rq.script}}');">حول</button><br /><br />
    <button id="exit" onClick="fb_exit();">اخرج</button><br /><br />
</div><!-- #menu -->
