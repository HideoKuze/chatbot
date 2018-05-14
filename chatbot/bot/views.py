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
from train_intent_parser import test_model
import codecs
import nltk
import spacy

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
CHATLIO_BOT_TOKEN = getattr(settings, 'CHATLIO_BOT_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)
#automatically searches for meta.json file
trained_model_path = 'C:/Users/Elitebook/Documents/Github/chatbot/chatbot/bot/'


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
			bot_text = 'hi'
			
			

			#sometimes you have to close the chat and refresh the page
			#finally use the slack api to post the message with chat.postMessage

			#get the subject from determine_subject()

			nlp = spacy.load(trained_model_path)
			#need to add 'root' to the beginning of the text because spaCy does not automatically label the first word as the root
			parsable_text = 'root ' + user_text
			bot_response = test_model(nlp, [parsable_text])

			try:
				Client.api_call(method='chat.postMessage',
					channel=channel,
					text=bot_response) 
				return Response(status=status.HTTP_200_OK)
			except Exception as e:
				Client.api_call(method='chat.postMessage',
					channel=channel,
					text=e) 
				return Response(status=status.HTTP_200_OK)

			'''if user_text == 'How do I delete my account?':
				Client.api_call(method='chat.postMessage',
					channel=channel,
					text=dependencies) 
				return Response(status=status.HTTP_200_OK)'''
		
		return Response(status=status.HTTP_200_OK)
