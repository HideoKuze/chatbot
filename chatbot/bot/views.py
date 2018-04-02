# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient
from models import Keywords, Responses
from serializers import KeywordsSerializer, ResponsesSerializer

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
CHATLIO_BOT_TOKEN = getattr(settings, 'CHATLIO_BOT_TOKEN', None)
Client = SlackClient(SLACK_BOT_USER_TOKEN)



# Create your views here.

class Events(APIView):
	def post(self, request, *args, **kwargs):


		slack_message = request.data

		#serialize the Python model data
		keywords_serializer = KeywordsSerializer.objects.all()
		bot_responses_serializer = ResponsesSerializer.objects.all()

		#render the Python data type into JSON
		keywords = JSONRenderer().render(keywords_serializer.data)
		bot_responses = JSONRenderer.render(bot_responses_serializer.data)

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
			text = event_message.get('text')
			channel = event_message.get('channel')
			bot_text = 'Hi there welcome to Proswap support, how may I help?'

			#sometimes you have to close the chat and refresh the page
			#finally use the slack api to post the message with chat.postMessage
			if 'hello' in text.lower():
				Client.api_call(method='chat.postMessage',
					channel=channel,
					text=bot_text) #this should be the output of word_processor?
				return Response(status=status.HTTP_200_OK)
		
		return Response(status=status.HTTP_200_OK)

		def word_processor(self, request, text):

			input_dictionary = {'hi': 'Hi there welcome to ProSwap support, how may I help?'}

			slack_message = request.data
			event_message = slack_message.get('event')
			text = slack_message.get('text')
			reply = ''

			for key in input_dictionary:
				if key = text:
					reply = input_dictionary[key]

			

		return Response(reply)