#!/usr/bin/python
# move_quran_db.py : move from sqlite to mysql

import db, os
import quran_db

db.setup_all()
quran_db.setup_all()

quran = quran_db.Quran.query.all()
sajadat = quran_db.Sajadat.query.all()
sura_info = quran_db.SuraInfo.query.all()
tahzeeb = quran_db.Tahzeeb.query.all()

c = 0
lc = c

for i in quran:
    cmd = u'INSERT INTO db_quran (othmani, imlai) values(\''+i.othmani+u'\',\''+ i.imlai+u'\');'
    os.system('echo "%s" >> insert.dat'%cmd.encode('utf8'))
    c += 1
    if c > (lc + 100):
        print '%s ayas moved to mysql db' %c
        lc = c
sc = 0
lsc = sc
for i in sura_info:
    if i.makki == None: makki = 'NULL'
    if i.comment == None: comment = ''
    cmd = u'INSERT INTO db_sura_info (sura_name, other_names, makki, starting_row, comment) values(\'%s\',\'%s\', %s, %s, \'%s\');'%(i.sura_name, i.other_names, makki, i.starting_row, comment)
    os.system('echo "%s" >> insert.dat'%cmd.encode('utf8'))
    sc += 1
    if c > (lsc + 10):
        print '%s suras moved to mysql db' %sc
        lsc = sc
tc = 0
ltc = tc
for i in tahzeeb:
    cmd = u'INSERT INTO db_tahzeeb (aya, sura) values(%s,%s);'%(i.aya, i.sura)
    os.system('echo "%s" >> insert.dat'%cmd.encode('utf8'))
    tc += 1
    if tc > (ltc + 10):
        print '%s tahzeeb moved to mysql db' %tc
        ltc = tc
sjc = 0
lsjc = sjc
for i in sajadat:
    cmd = u'INSERT INTO db_sajadat (sura, aya, sajda_type, comment) values(%s,%s, %s, \'%s\');'%(i.sura, i.aya, i.sajda_type, i.comment)
    os.system('echo "%s" >> insert.dat'%cmd.encode('utf8'))
    sjc += 1
    if sjc > (lsjc + 5):
        print '%s sajdah moved to mysql db' %sjc
        lsjc = sjc
print 'all finished, Done'
