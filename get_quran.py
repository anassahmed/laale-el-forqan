# -*- coding: UTF-8 -*-
#!/usr/bin/python
# get_quran.py: deal with quran_db.py

from db import *
import random
    
def get_random_aya(round):
    setup_all()
    if round.is_desc:
        from sqlalchemy import *
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
    return {'ayaId': a.id, 'ayaOthmani': a.othmani}

def validate_aya(ayaId, sura):
    setup_all()
    a = Quran.get_by(id = ayaId)
    s = SuraInfo.query.filter(SuraInfo.starting_row <= ayaId)[-1]
    if s.sura_name == sura:
        result = True
    else:
        result = False
    return {'result': result, 'sura': s.sura_name}
