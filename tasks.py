# Create a Celery Instance
from celery import Celery

# Connect to default RabbitMQ service
app = Celery('tasks', backend='amqp', broker='amqp://')

# Simple function that prints to the console
@app.task(ignore_result=True)
def print_hello():
    print 'hello there'


