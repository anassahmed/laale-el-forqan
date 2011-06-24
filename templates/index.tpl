<!DOCTYPE HTML>
<html>
	<head>
		<title>مسابقة لآليء الفرقان</title>
		<link href="{{rq.script}}/styles/style.css" rel="stylesheet" />
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
		<script type="text/javascript" src="{{rq.script}}/scripts/functions.js"></script>
		<script src="http://connect.facebook.net/ar_AR/all.js"></script>
		<script type="text/javascript">
		    FB.init({
                appId  : '211500928874964',
                status : true, // check login status
                cookie : true, // enable cookies to allow the server to access the session
                xfbml  : true  // parse XFBML
            });

            window.fbAsyncInit = function() {
                FB.Canvas.setSize({ width: 760, height: 900 }); // Live in the past
            };
        </script>
	</head>
	<body dir="rtl">
        <!-- [if IE]>
            <div id="no-ie" class="note">
            <p><strong>عزيزي مستخدم اﻹنترنت إكسبلورر:</strong> أنت تستخدم متصفحًا لا يدعم المعايير القياسية، ولا التقنيات الحديثة، لذا لن تستطيع دخول المسابقة إلا إذا استخدمت متصفحًا محترمًا مثل <a href="http://www.firefox.com">فَيَرْفُكْس</a> و<a href="http://chrome.google.com/">غوغل كروم</a>.</p>
            </div>
        <![endif]--> 
        %v = validate_auth(rq)
        %if v['is_authed']:
            %user = v['user']
            %include content rq=rq, args=args, user=user, heroes=heroes

        %else:
            <script type="text/javascript">
                var ie;
                ie = 0;
            </script>
            <!-- [if IE]>
                <script type="text/javascript">
                    ie = 1;
                </script>
            <![endif] -->
            <script type="text/javascript">
                if (!ie) {
                    top.location.href = '{{!v["auth_url"]}}';
                }
            </script>
            <div id="no-js" class="note">
            <p>مطلوب إذن! إذا لم يقم متصفحك بتحويلك للصفحة المطلوبة فاعلم أنك غير جدير بدخول هذه المسابقة باستخدام هذا المتصفح!</p>
            </div>

        %end
	</body>
</html>
