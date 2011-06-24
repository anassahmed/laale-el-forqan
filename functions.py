# -*- coding: UTF-8 -*-
# functions.py : functions used ferquently.

import os, base64, json, urllib, urllib2, datetime, random, facebook
from db_only import *
#from quran_db import *

appId = '211500928874964'
appSecret = 'e85ec6de300f949a8bcd888b9cb8648f'
canvasPage = 'http://apps.facebook.com/quran-quize/'
authUrl = 'http://www.facebook.com/dialog/oauth?client_id='+appId+'&redirect_uri='+urllib.quote(canvasPage)+'&scope=user_likes,read_stream,publish_stream,offline_access'

def decode_signed_request(signed_request):
    sep = signed_request.find('.')
    data = signed_request[sep:].replace('.','') + '='
    try:
        data = json.loads(base64.urlsafe_b64decode(data))
    except TypeError:
        data += '='
        data = json.loads(base64.urlsafe_b64decode(data))
    return data

def get_main_user_data(user_id, auth_token):
    graph = facebook.GraphAPI(auth_token)
    main_data = graph.get_object("me")
    return main_data

def change_access_token(user, oauth_token, expires):
    setup_all()
    u = users.get_by(id = user.id)
    u.access_token = oauth_token
    expires_date_time = datetime.datetime.utcfromtimestamp(expires)
    u.expires = expires_date_time
    session.commit()
    return True

def urlencode(url):
    return urllib.quote(url)

def get_user_by_fb_id(fb_id):
    setup_all()
    user = users.get_by(fb_id = fb_id)
    return user

def add_new_user(fb_id, fb_full_name, fb_user_name, oauth_token, expires, fb_gender, fb_locale):
    setup_all()
    expires_date_time = datetime.datetime.utcfromtimestamp(expires)
    user = users(fb_id = fb_id, fb_full_name = fb_full_name, fb_user_name = fb_user_name, access_token = oauth_token, expires = expires_date_time, fb_gender = fb_gender, fb_locale = fb_locale)
    a = statistics(user = user, rounds_num = 0, questions_num = 0, correct_answers = 0, wrong_answers = 0, points = 0, extra_points = 0, total_points = 0)
    session.commit()
    msg = "لقد بدأتُ إستخدام مسابقة لآلئ الفرقان، شاركوني المنافسة :) "
    s = publish_stream(user, msg)
    return user

def validate_auth(rq):
    setup_all()
    authUrl = 'http://www.facebook.com/dialog/oauth?client_id='+appId+'&redirect_uri='+urllib.quote(canvasPage)
    if rq.q.has_key('request_ids'):
        authUrl += urlencode('?request_ids='+rq.q.getfirst('request_ids'))
    authUrl += '&scope=user_likes,read_stream,publish_stream,offline_access'
    if rq.q.has_key('demo'):
    	user = users.get_by(fb_user_name = u"demo")
    	is_authed = 1
    elif rq.q.has_key('signed_request'):
        data = decode_signed_request(rq.q.getfirst('signed_request',''))
        try:
            main_user_data = get_main_user_data(data['user_id'], data['oauth_token'])
            user = get_user_by_fb_id(fb_id = data['user_id'].decode('utf8'))
            if user == None:
                try:
                    user_name = main_user_data['username']
                except KeyError:
                    user_name = u''
                user = add_new_user(fb_id = data['user_id'], fb_full_name = main_user_data['name'], fb_user_name = user_name, oauth_token = data['oauth_token'], expires = int(data['expires']), fb_gender = main_user_data['gender'], fb_locale = data['user']['locale'])
                if rq.q.has_key('request_ids'):
                    increase_points_invite(rq.q.getfirst('request_ids').decode('utf8'), user.fb_id)
            else:
                change_access_token(user, data['oauth_token'], int(data['expires']))
            is_authed = 1
        except KeyError:
            is_authed = 0 
            user = ''
    else: 
        is_authed = 0
        user = ''
    return {'is_authed':is_authed, 'auth_url':authUrl, 'user':user}

def get_statistics(user):
    setup_all()
    s = statistics.get_by(user = user)
    return s

def get_rank(user):
    setup_all()
    s = statistics.get_by(user = user)
    r = statistics.query.filter(statistics.total_points >= s.total_points).count()
    return r

def get_heroes():
    setup_all()
    from sqlalchemy import desc
    s = statistics.query.order_by(desc(statistics.total_points)).limit(5)
    return s

def create_new_round(user, parts_num, direction):
    setup_all()
    if direction == u'desc':
        is_desc = 1
    else: is_desc = 0
    r = rounds(user = user, parts_num = parts_num, is_desc = is_desc, question_num = 0, correct_answers = 0, wrong_answers = 0, points = 0, time = datetime.datetime.now(), is_finished = 0)
    session.commit()
    return r

def get_unfinished_round(user):
    setup_all()
    r = rounds.query.filter_by(user=user, is_finished = 0).first()
    return r

def get_round(round_id):
    setup_all()
    r = rounds.get_by(id = round_id)
    return r

def cancel_current_round(round):
    setup_all()
    round.is_finished = 1
    session.commit()
    return True


def publish_stream(user, message):
    setup_all()
    if user.fb_user_name == u"demo":
    	return False
    graph = facebook.GraphAPI(user.access_token)
    perms = graph.get_connections("me", "permissions")["data"][0]
    try:
        perm_publish = perms["publish_stream"]
        status_id = graph.put_object("me", "feed", message=message,\
        picture="http://www.darelnadwa.com/quran/images/Othman-128.png", \
        link="http://apps.facebook.com/quran-quize/", name="مسابقة لآلئ الفرقان", \
        caption="تطبيق فيسبوك.", description="""هذا التطبيق عبارة عن فكرة استلهمتُها من مسابقة خُضتها مع زملائي ونحن نراجع القرآن الكريم ليلة الإختبار، وكنا نفتح المصاحف بشكل عشوائي، والآية اللتي تقع عليها أعيننا، نسأل بعضنا عن السورة التي وردت فيها. وقد أعجبتني الفكرة ففكرت بتحويلها إلى تطبيق فيس بوك، يستفيد منه الكثير من الناس. """)
        return status_id["id"]
    except Exception:
        return False

def add_invite(rq):
    if rq.q.has_key('fb_user_id') and rq.q.has_key('request_ids'):
        setup_all()
        user = get_user_by_fb_id(rq.q.getfirst('fb_user_id','').decode('utf8'))
        request_ids = rq.q.getfirst('request_ids','').split(',')
        for i in request_ids:
            r = invites(user = user, fb_request_id = i.decode('utf8'), is_finished = 0)
            session.commit()
        r = {'result':True, 'requests':request_ids}
    else: r = {'result':False}
    return r

def increase_points_invite(rq_ids, fb_user_id):
    setup_all()
    request_ids = rq_ids.split(',')
    url_token = "https://graph.facebook.com/oauth/access_token?" + \
                    "client_id=" + appId + \
                    "&client_secret=" + appSecret + \
                    "&grant_type=client_credentials"
    app_token = urllib2.urlopen(url_token).read()
    inv_id = invites.get_by(fb_friend_id = fb_user_id)
    if inv_id == None:
        for i in request_ids:
            inv = invites.get_by(fb_request_id = i)
            if inv != None:
                if not inv.is_finished:
                    s = statistics.get_by(user = inv.user)
                    s.extra_points += 100
                    s.total_points += 100
                    inv.fb_friend_id = fb_user_id
                    inv.is_finished = 1
                    session.commit()
                    try:
                        deleted = urllib2.urlopen("https://graph.facebook.com/"+i.encode('utf8')+"?"+app_token+"&method=delete")
                    except HTTPError:
                        pass
                    break
                    return True
                else: continue
            else: continue
    return False

def get_suras(round):
    setup_all()
    if round == None: return []
    if round.is_desc:
        from sqlalchemy import desc
        t = Tahzeeb.query.order_by(desc(Tahzeeb.sura)).limit(round.parts_num*8+1)[-1]
    else:
        t = Tahzeeb.query.limit(round.parts_num*8+1)[-1]
    s = SuraInfo.get_by(id = t.sura)
    if round.is_desc:
        suras_query = SuraInfo.query.filter(SuraInfo.id >= s.id).all()
    else:
        suras_query = SuraInfo.query.filter(SuraInfo.id <= s.id).all()
    suras = []
    for i in suras_query:
        suras.append(i.sura_name)
    return suras

def get_random_aya(round):
    setup_all()
    if round.is_desc:
        from sqlalchemy import desc
        t = Tahzeeb.query.order_by(desc(Tahzeeb.sura)).limit(round.parts_num*8+1)[-1]
    else:
        t = Tahzeeb.query.limit(round.parts_num*8+1)[-1]
    s = SuraInfo.get_by(id = t.sura)
    if round.is_desc:
        sa = Quran.get_by(id = s.starting_row+t.aya-1)
        ea = Quran.get_by(id = 6236)
    else:
        sa = Quran.get_by(id = 2)
        ea = Quran.get_by(id = s.starting_row+t.aya-1)
    a = Quran.get_by(id = random.randint(sa.id, ea.id))
    a_sura = SuraInfo.query.filter(SuraInfo.starting_row <= a.id)[-1]
    a_num = a_sura.starting_row - a.id
    a_text = a.othmani
    if a_num < 10:
    	a_text = a.othmani[:-4]
    elif a_num < 100:
    	a_text = a.othmani[:-5]
    elif a_num < 1000:
    	a_text = a.othmani[:-6]
    return {'ayaId': a.id, 'ayaOthmani': a_text}

def validate_aya(ayaId, sura):
    setup_all()
    a = Quran.get_by(id = ayaId)
    s = SuraInfo.query.filter(SuraInfo.starting_row <= ayaId)[-1]
    if s.sura_name == sura:
        result = True
    else:
        result = False
    return {'result': result, 'sura': s.sura_name}

def json_page(rq, args):
    setup_all()
    r = rounds.get_by(id = int(rq.q.getfirst('roundId','')))
    if args:
        if args[0] == 'get_random_aya':
            re = get_random_aya(r)
            reply = {'ayaId':re['ayaId'], 'ayaOthmani': re['ayaOthmani']}
        elif args[0] == 'validate_aya':
            a = validate_aya(int(rq.q.getfirst('ayaId', '')), rq.q.getfirst('sura','').decode('utf8'))
            r.question_num += 1
            if a['result'] == True:
                r.correct_answers += 1
                r.points += r.parts_num
                p = r.parts_num * 10
                if r.points == p:
                    r.is_finished = 1
                    s = statistics.get_by(user = r.user)
                    s.rounds_num += 1
                    s.questions_num += r.question_num
                    s.correct_answers += r.correct_answers
                    s.wrong_answers += r.wrong_answers
                    s.points += r.points
                    s.total_points += r.points
                    msg = "لقد أحرزتُ انتصارًا جديدًا في إحدى جولات مسابقة لآلئ الفرقان الجديدة، عدد الأجزاء: %d، عدد الأسئلة: %d، الإجابات الصحيحة: %d، الإجابات الخاطئة: %d، النقاط: %d. شاركوني!" %(r.parts_num, r.question_num, r.correct_answers, r.wrong_answers, r.points)
                    status_id = publish_stream(r.user, msg)
                    if s.user.fb_user_name == u"demo" and s.total_points >= 500:
                    	s.rounds_num = 0
                    	s.questions_num = 0
                    	s.correct_answers = 0
                    	s.wrong_answers = 0
                    	s.points = 0
                    	s.total_points = 0
                    	rs = rounds.filter(rounds.user.fb_user_name == u"demo").all()
                    	for i in rs:
                    		i.delete()
                    	session.commit()
            else:
                r.wrong_answers += 1
                r.points -= r.parts_num
            session.commit()
            reply = {'result': a['result'], 'question_num': r.question_num, 'correct_answers': r.correct_answers, 'wrong_answers': r.wrong_answers, 'points': r.points, 'is_finished': r.is_finished, 'correctSura': a['sura']}
        elif args[0] == 'cancel_round':
            r.is_finished = 1
            session.commit()
            reply = {'result':True}
        else: reply = 0
    else: reply = 0
    return reply