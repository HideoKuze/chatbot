import mysql.connector
import json
from datetime import datetime
import os

cnx = mysql.connector.connect(user='root', password='gits2501',
	host='localhost', database='chatbot')
cursor = cnx.cursor()

sql_transaction = []
datasets = ['conversation_data']
#have a list of all intents so we can iterate through them and create their respective tables

#insert the dataset into the database
def create_table():
	op = '''CREATE TABLE conversation (
	text TEXT NOT NULL,
	intent TEXT NOT NULL,
	entities TEXT,
	reply TEXT NOT NULL,
	)'''
	cursor.execute(op)
	

#only accept data that is of certain length
def acceptable(data):
	if len(data.split(' ')) > 40 or len(data) < 2:
		return False
	elif len(data) > 300:
		return False
	else:
		return True

#format the data so newlines are replaced with a space
def format_data(data):
	data = data.replace("\n", " ").replace("\r", " ").replace('"', "'")

def transaction_builder(sql, text, intent, entities, reply):
	global sql_transaction
	sql_transaction.append(sql)

	if len(sql_transaction) > 0:
		cursor.execute('START TRANSACTION')
		for s in sql_transaction:
			try:
				#use arguments in execution instead to avoid SQL injections https://docs.djangoproject.com/en/1.11/topics/db/sql/
				cursor.execute(s, (text, intent, entities, reply))
			except Exception as e:
				print e

		cnx.commit()
		sql_transaction = []

def insert_message(text, intent, entities, reply):
	try:
		#avoid using placeholders to avoid SQL injection, will pass text, intent and entities to transaction_builder() instead
		sql = """INSERT INTO conversation  (text, intent, entities, reply) VALUES (%s, %s, %s, %s)"""
		transaction_builder(sql, text, intent, entities, reply)
	except Exception as e:
		print ('error is', str(e))


if __name__ == "__main__": 
	create_table()

	#iterate through the list of datasets 
	for dataset in datasets:
		with open('C:/Users/ELITEBOOK/documents/github/chatbot/chatbot/bot/{}'.format(dataset), 'r') as table:
			for properties in table:
				properties = json.loads(properties)
				content = properties['property']

				for messages in content:
					if acceptable(messages['text']):
						message_text = messages['text']
						message_intent = messages['intent']
						message_entities = messages['entities']
						message_reply = messages['reply']

						insert_message(message_text, message_intent, message_entities, message_reply)

