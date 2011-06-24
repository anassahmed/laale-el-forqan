# -*- coding: UTF-8 -*-
# main.py : the main file.

from okasha.baseWebApp import *
from okasha.bottleTemplate import *
from functions import *

class quran_quiz(baseWebApp):
    def __init__(self, *args, **kw):
        baseWebApp.__init__(self, *args, **kw)
    
    @expose(bottleTemplate, ['index.tpl'])
    def _root(self, rq, *args):
        return {'rq':rq, 'args':args, 'validate_auth':validate_auth, 'heroes':get_heroes()}
        
    @expose(bottleTemplate, ['menu.tpl'])
    def menu(self, rq, *args):
        if rq.q.has_key('fb_user_id'):
            user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
        else:
            raise forbiddenExeption()
        return {'rq':rq, 'args':args, 'user':user}
    
    @expose(bottleTemplate, ['about.tpl'])
    def about(self, rq, *args):
        return {'rq':rq, 'args':args}
    
    @expose(bottleTemplate, ['statistics.tpl'])
    def statistics(self, rq, *args):
        if rq.q.has_key('fb_user_id'):
            user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
            s = get_statistics(user)
            rank = get_rank(user)
            return {'rq':rq, 'args':args, 'user':user, 'statistics':s, 'rank':rank}
        if rq.q.has_key('round_id'):
            r = get_round(round_id = int(rq.q.getfirst('round_id')))
            return {'rq':rq, 'args':args, 'r':r}
        return {'rq':rq, 'args':args}
    
    @expose(bottleTemplate, ['rounds.tpl'])
    def rounds(self, rq, *args):
        if rq.q.has_key('fb_user_id'):
            user = get_user_by_fb_id(rq.q.getfirst('fb_user_id').decode('utf8'))
        else:
            raise forbiddenExeption()

        if rq.q.has_key('parts_num'):
            r = create_new_round(user = user, parts_num = int(rq.q.getfirst('parts_num')), direction = rq.q.getfirst('direction','').decode('utf8'))
        else:
            r = get_unfinished_round(user)
        return {'rq':rq, 'args':args, 'user':user, 'round':r, 'suras':get_suras(r)}
    
    @expose(jsonDumps)
    def json(self, rq, *args):
        reply = json_page(rq, args)
        if reply != 0:
            return reply
        else:
            raise forbiddenException()

    @expose(jsonDumps)
    def invite(self, rq, *args):
        i = add_invite(rq)
        return i
