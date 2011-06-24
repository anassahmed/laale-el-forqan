# -*- coding: UTF-8 -*-
# db.py: database schema

from elixir import *
import os, os.path

db_server = 'localhost'
db_user = 'anass'
db_pass = 'anass=1430'
db_name = 'quran'
db_prefix = 'db_'

db_mysql_path = 'mysql://%s:%s@%s/%s' %(db_user, db_pass, db_server, db_name)
db_sqlite_path = "sqlite:///"+os.path.expanduser("~/python-modules/quran_quize/db.db")

metadata.bind = db_sqlite_path

class users(Entity):
    using_options(tablename = db_prefix+'users')
    fb_id = Field(Unicode(100))
    fb_user_name = Field(UnicodeText)
    fb_full_name = Field(UnicodeText)
    fb_gender = Field(Unicode(10))
    fb_locale = Field(Unicode(5))
    access_token = Field(UnicodeText)
    expires = Field(DateTime)

class rounds(Entity):
    using_options(tablename = db_prefix+'rounds')
    user = ManyToOne('users')
    parts_num = Field(Integer)
    is_desc = Field(Integer)
    question_num = Field(Integer)
    correct_answers = Field(Integer)
    wrong_answers = Field(Integer)
    points = Field(Integer)
    time = Field(DateTime)
    is_finished = Field(Integer)

class statistics(Entity):
    using_options(tablename = db_prefix+'statistics')
    user = ManyToOne('users')
    rounds_num = Field(Integer)
    questions_num = Field(Integer)
    correct_answers = Field(Integer)
    wrong_answers = Field(Integer)
    points = Field(Integer)
    extra_points = Field(Integer)
    total_points = Field(Integer)

class invites(Entity):
    using_options(tablename = db_prefix+'invites')
    user = ManyToOne('users')
    fb_request_id = Field(Unicode(100))
    fb_friend_id = Field(Unicode(100))
    is_finished = Field(Integer)

class Quran(Entity):
    using_options(tablename = db_prefix+'quran')
    id = Field(Integer, primary_key = True)
    othmani = Field(UnicodeText)
    imlai = Field(UnicodeText)

class Sajadat(Entity):
    using_options(tablename = db_prefix+'sajadat')
    id = Field(Integer, primary_key = True)
    sura = Field(Integer,index = True, primary_key = True)
    aya = Field(Integer)
    sajda_type = Field(Integer)
    comment = Field(UnicodeText)

class SuraInfo(Entity):
    using_options(tablename = db_prefix+'sura_info')
    id = Field(Integer, primary_key = True)
    sura_name = Field(UnicodeText, primary_key = True)
    other_names = Field(UnicodeText)
    makki = Field(Integer)
    starting_row = Field(Integer)
    comment = Field(UnicodeText)

class Tahzeeb(Entity):
    using_options(tablename = db_prefix+'tahzeeb')
    id = Field(Integer, primary_key = True)
    sura = Field(Integer,index = True, primary_key = True)
    aya = Field(Integer, primary_key = True)
