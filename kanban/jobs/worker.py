from celery import Celery

REDIS_URL = 'redis://localhost:6379/1'

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SMTP_SENDER_ADDRESS = 'kanban@example.com'
SMTP_SENDER_PASSWORD = ''

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL, include=['kanban.jobs.tasks'])

if __name__ == '__main__':
    celery.start()
