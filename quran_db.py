#!/usr/bin/python
# quran_db.py: move quran.db to mysql db

from elixir import *

metadata.bind = 'sqlite:///quran.db'

class Quran(Entity):
    using_options(tablename = 'Quran')
    othmani = Field(UnicodeText)
    imlai = Field(UnicodeText)

class Sajadat(Entity):
    using_options(tablename = 'Sajadat')
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
    sura = Field(Integer,index = True, primary_key = True)
    aya = Field(Integer, primary_key = True)
