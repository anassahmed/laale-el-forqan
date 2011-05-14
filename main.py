# -*- coding: UTF-8 -*-
#!/usr/bin/python
# main.py : the main file.

from okasha.baseWebApp import *
from okasha.bottleTemplate import *
from db import *
from functions import *

class quran_quiz(baseWebApp):
    def __init__(self, *args, **kw):
        baseWebApp.__init__(self, *args, **kw)
    
    @expose(bottleTemplate, ['index.tpl'])
    def _root(self, rq, *args):
        return {'rq':rq, 'args':args}
        
    @expose(bottleTemplate, ['menu.tpl'])
    def menu(self, rq, *args):
        return {'rq':rq, 'args':args}
    
    @expose(bottleTemplate, ['about.tpl'])
    def about(self, rq, *args):
        return {'rq':rq, 'args':args}
    
    @expose(bottleTemplate, ['statistics.tpl'])
    def statistics(self, rq, *args):
        return {'rq':rq, 'args':args}
    
    @expose(bottleTemplate, ['rounds.tpl'])
    def rounds(self, rq, *args):
        return {'rq':rq, 'args':args}
    
    @expose(jsonDumps)
    def json(self, rq, *args):
        setup_all()
        r = rounds.get_by(id = int(rq.q.getfirst('roundId','')))
        if args:
            if args[0] == 'get_random_aya':
                re = get_random_aya(r)
                return {'ayaId':re['ayaId'], 'ayaOthmani': re['ayaOthmani']}
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
                else:
                    r.wrong_answers += 1
                    r.points -= r.parts_num
                session.commit()
                return {'result': a['result'], 'question_num': r.question_num, 'correct_answers': r.correct_answers, 'wrong_answers': r.wrong_answers, 'points': r.points, 'is_finished': r.is_finished, 'correctSura': a['sura']}
            else: raise forbiddenException()
        else:
            raise forbiddenException()

    @expose(jsonDumps)
    def invite(self, rq, *args):
        if rq.q.has_key('fb_user_id') and rq.q.has_key('request_ids'):
            setup_all()
            user = get_user_by_fb_id(rq.q.getfirst('fb_user_id','').decode('utf8'))
            request_ids = rq.q.getfirst('request_ids','').split(',')
            for i in request_ids:
                r = invites(user = user, fb_request_id = i.decode('utf8'), is_finished = 0)
                session.commit()
            return {'result': True, 'requests':request_ids}
        else:
            return {'result': False}
