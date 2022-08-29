from datetime import datetime, date
from humanize import naturaldate, precisedelta


def today():
    return date.today()


def greeting_text(name):
    hour = datetime.now().hour
    if hour < 12:
        greeting = 'Good morning'
    elif 12 <= hour <= 17:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    return f'{greeting}, {name}'


def date_text(value, relative=False):
    if relative:
        return precisedelta(date.today() - value).capitalize()
    else:
        return naturaldate(value).capitalize()
