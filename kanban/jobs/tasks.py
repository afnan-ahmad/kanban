from .worker import *

from csv import DictWriter
from io import StringIO

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from kanban.models.user import User
from kanban.models.list import List

LIST_FIELD_NAMES = ['id', 'name', 'no_of_cards']
CARD_FILED_NAMES = ['id', 'title', 'content', 'deadline', 'completed']


def send_email(to, subject, csv):
    email = MIMEMultipart()
    email['From'] = SMTP_SENDER_ADDRESS
    email['To'] = to
    email['Subject'] = subject

    csv_part = MIMEText(csv['data'], 'csv')
    csv_part.add_header('Content-Disposition', f"attachment; filename={csv['filename']}")

    email.attach(csv_part)

    s = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    s.login(SMTP_SENDER_ADDRESS, SMTP_SENDER_PASSWORD)

    s.send_message(email)
    s.quit()


@celery.task
def export_lists(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return

    output = StringIO()

    writer = DictWriter(output, fieldnames=LIST_FIELD_NAMES)
    writer.writeheader()

    user_lists = List.query.filter_by(user_id=user.id).all()

    if not user_lists:
        return

    for lst in user_lists:
        writer.writerow({'id': lst.id,
                         'name': lst.name,
                         'no_of_cards': len(lst.cards)})

    send_email(user.email, '[Kanban] Board export completed', {
        'data': output.getvalue(),
        'filename': 'kanban_export.csv'
    })

    output.close()


@celery.task
def export_cards(list_id):
    lst = List.query.filter_by(id=list_id).first()
    if not lst:
        return

    user = User.query.filter_by(id=lst.user_id).first()
    if not user:
        return

    output = StringIO()

    writer = DictWriter(output, fieldnames=CARD_FILED_NAMES)
    writer.writeheader()

    if not lst.cards:
        return

    for card in lst.cards:
        writer.writerow({'id': card.id,
                         'title': card.title,
                         'content': card.content,
                         'deadline': card.deadline,
                         'completed': card.completed})

    send_email(user.email, '[Kanban] List export completed', {
        'data': output.getvalue(),
        'filename': 'kanban_list_export.csv'
    })

    output.close()
