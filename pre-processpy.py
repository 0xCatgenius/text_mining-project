# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 22:19:07 2019

@author: malcolmng.2015
"""

import re, string, unicodedata
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import pandas as pd
from textblob import TextBlob as tb
from textblob import Word 

text_list = []
sentence_list = []
train = pd.read_csv('data/Review.csv')
text_list = train['Text'].apply(lambda x: " ".join(x.lower() for x in x.split()))

r1 = text_list[0]
r1 = tb(r1)

for r in text_list:
    r_curr = tb(r)
    r_sent = r_curr.sentences
    for s in r_sent:
        sentence_list.append(str(s))
