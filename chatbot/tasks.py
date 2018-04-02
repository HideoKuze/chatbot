from celery import Celery

#first argument is the name of the module
app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
	return x + y