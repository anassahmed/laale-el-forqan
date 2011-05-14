<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:og="http://ogp.me/ns#"
      xmlns:fb="http://www.facebook.com/2008/fbml">
	<head>
		<title>مسابقة لآليء الفرقان</title>
		<meta property="og:title" content="مسابقة لآلئ الفرقان"/>
        <meta property="og:type" content="game"/>
        <meta property="og:url" content="http://apps.facebook.com/quran-quize/"/>
        <meta property="og:image" content="{{rq.script}}/images/Othman-128.png"/>
        <meta property="og:site_name" content="لآليء الفرقان"/>
        <meta property="fb:app_id" content="211500928874964"/>
        <meta property="og:description"
              content="هذا التطبيق عبارة عن فكرة استلهمتُها من مسابقة خُضتها مع زملائي ونحن نراجع القرآن الكريم ليلة الإختبار، وكنا نفتح المصاحف بشكل عشوائي، والآية اللتي تقع عليها أعيننا، نسأل بعضنا عن السورة التي وردت فيها. وقد أعجبتني الفكرة ففكرت بتحويلها إلى تطبيق فيس بوك، يستفيد منه الكثير من الناس."/>
		<link href="{{rq.script}}/styles/style.css" rel="stylesheet" />
		<script type="text/javascript" src="{{rq.script}}/scripts/jquery-1.5.1.min.js"></script>
		<script type="text/javascript" src="{{rq.script}}/scripts/functions.js"></script>
		<script src="{{rq.script}}/scripts/jquery.ui.draggable.js" type="text/javascript"></script>
		<script src="{{rq.script}}/scripts/jquery.alerts.js" type="text/javascript"></script>
		<link href="{{rq.script}}/styles/css.css" rel="stylesheet" type="text/css" media="screen" />
		<script src="http://connect.facebook.net/en_US/all.js"></script>
		<script type="text/javascript">
		    FB.init({
                appId  : '211500928874964',
                status : true, // check login status
                cookie : true, // enable cookies to allow the server to access the session
                xfbml  : true  // parse XFBML
            });
        </script>
	</head>
	<body dir="rtl">
        %from functions import *
        %appId = '211500928874964'
        %canvasPage = 'http://apps.facebook.com/quran-quize/'
        %authUrl = 'http://www.facebook.com/dialog/oauth?client_id='+appId+'&redirect_uri='+urlencode(canvasPage)
        %if rq.q.has_key('request_ids'):
            %authUrl += urlencode('?request_ids='+rq.q.getfirst('request_ids'))
        %end
        %authUrl += '&scope=user_likes,read_stream,publish_stream'
        %if rq.cookies.has_key('fb_qq_user_id'):
            %user_id = rq.cookies['fb_qq_user_id'].value.decode('utf8')
            %user = get_user_by_fb_id(user_id)
            %include content user = user, rq = rq, args = args
        %elif rq.q.has_key('signed_request'):
            %data = decode_signed_request(rq.q.getfirst('signed_request',''))
            %try:
                %main_user_data = get_main_user_data(data['user_id'], data['oauth_token'])
                %user = get_user_by_fb_id(fb_id = data['user_id'])
                %if user == None:
                    %try:
                        %user_name = main_user_data['username']
                    %except KeyError:
                        %user_name = u''
                    %end
                    %user = add_new_user(fb_id = data['user_id'], fb_full_name = main_user_data['name'], fb_user_name = user_name, oauth_token = data['oauth_token'], expires = int(data['expires']), fb_gender = main_user_data['gender'], fb_locale = data['user']['locale'])
                    %if rq.q.has_key('request_ids'):
                        %increase_points_invite(rq.q.getfirst('request_ids').decode('utf8'), user.fb_id)
                    %end
                %else:
                    %change_access_token(user, data['oauth_token'], int(data['expires']))
                %end
                %set_cookie(rq, data)
                %include content user = user, rq = rq, args = args
            %except KeyError:
                <script type="text/javascript">
                    top.location.href = '{{!authUrl}}'
                </script>
                <p>مطلوب إذن! إذا لم يقم متصفحك بتحويلك للصفحة المطلوبة فاعلم أنك غير جدير بدخول هذه المسابقة باستخدام هذا المتصفح!</p>
            %end
        %else:
            <script type="text/javascript">
                top.location.href = '{{!authUrl}}'
            </script>
            <p>مطلوب إذن! إذا لم يقم متصفحك بتحويلك للصفحة المطلوبة فاعلم أنك غير جدير بدخول هذه المسابقة باستخدام هذا المتصفح!</p>
        %end
	</body>
</html>
