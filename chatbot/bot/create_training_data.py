# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mysql.connector
import json
from datetime import datetime
import os
import pandas as pd
import codecs
import spacy

'''datasets = ['conversation_data']

for dataset in datasets:
	cnx = mysql.connector.connect(user='root', password='gits2501',
	host='localhost', database='chatbot')
	cursor = cnx.cursor()

	#dataframe
	df = pd.read_sql('SELECT * FROM conversation', cnx)

	with codecs.open("C:/Users/ELITEBOOK/documents/github/chatbot/chatbot/bot/chat.from", 'a', encoding='utf8') as f:
		for content in df['text'].values:
			f.write(content+'\n')
	with codecs.open("C:/Users/ELITEBOOK/documents/github/chatbot/chatbot/bot/chat.to", 'a', encoding='utf8') as f:
		for content in df['reply'].values:
			f.write(content+'\n')'''


import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u"root delete my account")
for token in doc:
    print token.head.text
