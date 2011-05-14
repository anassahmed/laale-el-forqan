<!-- Honor Board -->

%from functions import *

<div id="honorBoard" class="honorBoard">
    <h3> لوحة الشرف </h3>
	%heros = get_heros()
	%rank = 0
	%for i in heros:
	    %rank += 1
		<div id="hero" class="hero">
			<a href="http://www.facebook.com/profile.php?id={{i.fb_id}}" title="الملف الشخصي"><img src="http://graph.facebook.com/{{i.fb_id}}/picture/" />{{i.fb_full_name}}</a>
			<br />
			<p>المرتبة: {{rank}}</p>
		</div>
    %end
</div>
