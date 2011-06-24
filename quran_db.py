# quran_db.py: move quran.db to mysql db

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.schema import ThreadLocalMetaData
from elixir import *
import os, os.path

a_engine = create_engine('sqlite:///'+os.path.expanduser("~/python-modules/quran_quize/quran.db"))
a_session = scoped_session(sessionmaker(autoflush=True))
a_metadata = metadata

__metadata__ = a_metadata
__session__ = a_session

a_metadata.bind = a_engine
a_session.bind = a_engine


class Quran(Entity):
    using_options(tablename = 'Quran')
    rowid = Field(Integer, primary_key = True)
    othmani = Field(UnicodeText)
    imlai = Field(UnicodeText)

class Sajadat(Entity):
    using_options(tablename = 'Sajadat')
    rowid = Field(Integer, primary_key = True)
    sura = Field(Integer,index = True, primary_key = True)
    aya = Field(Integer)
    sajda_type = Field(Integer)
    comment = Field(UnicodeText)

class SuraInfo(Entity):
    using_options(tablename = 'SuraInfo')
    rowid = Field(Integer, primary_key = True)
    sura_name = Field(UnicodeText, primary_key = True)
    other_names = Field(UnicodeText)
    makki = Field(Integer)
    starting_row = Field(Integer)
    comment = Field(UnicodeText)

class Tahzeeb(Entity):
    using_options(tablename = 'Tahzeeb')
    rowid = Field(Integer, primary_key = True)
    sura = Field(Integer,index = True, primary_key = True)
    aya = Field(Integer, primary_key = True)
