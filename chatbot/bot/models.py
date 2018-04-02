# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Entities(models.Model):
	#this will be a model that will store information about keywords)entities) used in inquiries from users
	user_text = models.CharField(max_length=20)


class Responses(models.Model):
	bot_responses = models.TextField()
	