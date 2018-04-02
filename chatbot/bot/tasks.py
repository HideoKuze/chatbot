from celery import task
import django
django.setup()

#first argument is the name of the module
broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'


@task()
def all_user_messages(user):
	
	