# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient
import mysql.connector
import json
from datetime import datetime
import os
from itertools import izip #for iterating files in parallel
import codecs
import nltk
import spacy

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
CHATLIO_BOT_TOKEN = getattr(settings, 'CHATLIO_BOT_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)



# Create your views here.

class Events(APIView):
	def post(self, request, *args, **kwargs):


		slack_message = request.data

		#serialize the Python model data
		#keywords_serializer = KeywordsSerializer.objects.all()
		#bot_responses_serializer = ResponsesSerializer.objects.all()

		#render the Python data type into JSON
		#keywords = JSONRenderer().render(keywords_serializer.data)
		#bot_responses = JSONRenderer.render(bot_responses_serializer.data)

		#verify token
		if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
			return Response(status=status.HTTP_403_FORBIDDEN)

		#checking for url verification
		if slack_message.get('type') == 'url_verification':
			return Response(data=slack_message, status=status.HTTP_200_OK)

		#send a greeting to the bot
		if 'event' in slack_message:
			#process message if event data is contained in it
			event_message = slack_message.get('event')


			#handle the message by parsing the JSON data
			user = event_message.get('user')
			user_text = event_message.get('text')
			channel = event_message.get('channel')
			bot_text = ''
			
			

			#sometimes you have to close the chat and refresh the page
			#finally use the slack api to post the message with chat.postMessage


			intents = {
			'greet':['hey','howdy', 'hey there','hello', 'hi'],
			'deposit':['You can do so here: placeholder.com'],
			'feedback':['You can do so here: placeholder.com'],
			'fee': ['fee', 'charge', 'price'],
			'influence-score': ['impact', 'score'],
			'delete' : ['delete', 'remove', 'rid']
			}

			#get the subject from determine_subject()
			subject = determine_subject(user_text)

			try:
				with codecs.open('C:/Users/ELITEBOOK/documents/github/chatbot/chatbot/bot/chat.from', 'r', encoding='utf8') as table2, codecs.open('C:/Users/ELITEBOOK/documents/github/chatbot/chatbot/bot/chat.to','r', encoding='utf8') as table3:
					for human_line, robo_line in zip(table2,table3):
						#have to use split() to remove the space that appears when reading a file
						for keys in intents:
							if user_text.split()[0] in intents[keys]:
								print True
								break
																				
			except Exception, e:
				raise e
			 
			Client.api_call(method='chat.postMessage',
				channel=channel,
				text=bot_text) 
			return Response(status=status.HTTP_200_OK)
		
		return Response(status=status.HTTP_200_OK)

		def determine_subject(sentence):
			nlp = spacy.load('en')
			tokens = nlp(sentence) #tokenize the text

			for token in tokens:
				#find the subject
				if token.dep_ == 'nsubj':
					subject = token.dep_
					return subject