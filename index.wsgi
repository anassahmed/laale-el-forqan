# -*- coding: UTF-8 -*-
import sys, os, os.path
d=os.path.dirname(__file__)
sys.path.append(d)
from main import quran_quiz
application=quran_quiz(
  os.path.join(d,'templates'),
  staticBaseDir={'/files/':os.path.join(d,'files'),
  '/styles/':os.path.join(d, 'files', 'styles'),
  '/images/':os.path.join(d, 'files', 'images'),
  '/scripts/':os.path.join(d, 'files', 'scripts'),
  '/audios/':os.path.join(d, 'files', 'audios')}
);
