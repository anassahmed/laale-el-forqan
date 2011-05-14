# -*- coding: UTF-8 -*-
#!/usr/bin/python
# functions.py : functions used ferquently.

import base64, json, urllib, urllib2, datetime, get_quran
from db import *

appId = '211500928874964'
appSecret = 'e85ec6de300f949a8bcd888b9cb8648f'
canvasPage = 'http://apps.facebook.com/quran-quize/'
authUrl = 'http://www.facebook.com/dialog/oauth?client_id='+appId+'&redirect_uri='+urllib.quote(canvasPage)+'&scope=user_likes,read_stream,publish_stream'

def decode_signed_request(signed_request):
    sep = signed_request.find('.')
    data = signed_request[sep:].replace('.','') + '='
    data = json.loads(base64.urlsafe_b64decode(data))
    return data

def get_main_user_data(user_id, auth_token):
    main_js_data = urllib2.urlopen('https://graph.facebook.com/'+user_id+'?access_token='+auth_token).read()
    main_data = json.loads(main_js_data)
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

def set_cookie(rq, data):
    expires_date_time = datetime.datetime.utcfromtimestamp(int(data['expires']))
    expires = expires_date_time - datetime.datetime.now()
    rq.response.setCookie('fb_qq_user_id', data['user_id'], expires.seconds)
    return True

def get_access_token(rq, user):
    setup_all()
    now = datetime.datetime.now()
    if user.expires < now:
        u = urllib.urlopen(authUrl).read()
        s = decode_signed_request(u)
        access_token = s['oauth_token']
        user.access_token = access_token
        session.commit()
        set_cookie(rq, s)
        return access_token
    else:
        return user.access_token

def add_new_user(fb_id, fb_full_name, fb_user_name, oauth_token, expires, fb_gender, fb_locale):
    setup_all()
    expires_date_time = datetime.datetime.utcfromtimestamp(expires)
    user = users(fb_id = fb_id, fb_full_name = fb_full_name, fb_user_name = fb_user_name, access_token = oauth_token, expires = expires_date_time, fb_gender = fb_gender, fb_locale = fb_locale)
    a = statistics(user = user, rounds_num = 0, questions_num = 0, correct_answers = 0, wrong_answers = 0, points = 0, extra_points = 0, total_points = 0)
    session.commit()
    return user

def add_points_invite(id):
    setup_all()
    invite = invites.get_by(id = id)
    if invite != None:
        if not invite.is_finished:
            s = statistics.get_by(user = invite.user)
            s.extra_points += 100
            invite.is_finished = 1
            session.commit()
            return True
        else:
            return False
    else: return False

def get_statistics(user):
    setup_all()
    s = statistics.get_by(user = user)
    return s

def get_heros():
    setup_all()
    from sqlalchemy import desc
    s = statistics.query.order_by(desc(statistics.total_points)).limit(5)
    us = []
    for i in s:
        us.append(i.user)
    return us

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

def get_suras():
    setup_all()
    suras = []
    for i in SuraInfo.query.all():
        suras.append(i.sura_name)
    return suras

def publish_stream(rq, user):
    setup_all()
    access_token = get_access_token(rq, user, message)
    params = urllib.urlencode('message=%s' \
    'link=http://apps.facebook.com/quran-quize/' \
    'picture=http://apps.facebook.com/quran-quize/images/Othman-128.png' \
    'name=مسابقة لآلئ الفرقان' \
    'caption=مسابقة لآلئ الفرقان' \
    'description=مسابقة لاختبار حفظك في عدد من الأجزاء تحدده، وبناءًا على إجاباتك تحدد نقاطك، وتوضع في لوحة الشرف مع أصدقائك!' \
    'actions={"name": "مسابقة ﻵلئ الفرقان", "link": "http://www.zombo.com"}' \
    'privacy={"value": "ALL_FRIENDS"}' %message)
    u = urllib2.urlopen('https://graph.facebook.com/%s/feed%s' %(user.fb_user_id, params))

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

get_random_aya = get_quran.get_random_aya
validate_aya = get_quran.validate_aya
