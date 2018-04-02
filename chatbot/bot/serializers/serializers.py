#serializers

from .models import Keywords, Responses
from rest_framework import serializers

class KeywordsSerializer(serializers.Serializer):

	class Meta:
		model = Keywords

		fields = ['user_text']


class ResponsesSerializer(serializers.Serializer):

	class Meta:
		model = Responses

		field = ['bot_responses']