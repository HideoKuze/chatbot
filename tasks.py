from celery import Celery
import django
django.setup()

#first argument is the name of the module
broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
	return x + y