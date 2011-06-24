# -*- coding: UTF-8 -*-
# db.py: database schema

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.schema import ThreadLocalMetaData
from elixir import *
import os, os.path

db_server = 'localhost'
db_user = 'anass'
db_pass = 'anass=1430'
db_name = 'quran'
db_prefix = 'db_'

db_mysql_path = 'mysql://%s:%s@%s/%s' %(db_user, db_pass, db_server, db_name)
db_sqlite_path = "sqlite:///"+os.path.expanduser("~/python-modules/quran_quize/db.db")

b_engine = create_engine(db_mysql_path)
b_session = scoped_session(sessionmaker(autoflush=True))
b_metadata = ThreadLocalMetaData() 

__metadata__ = b_metadata
__session__ = b_session

b_metadata.bind = b_engine
b_session.bind = b_engine

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
