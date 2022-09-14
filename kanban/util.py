from datetime import date
from humanize import naturaldate, precisedelta


def today():
    return date.today()


def date_text(value, relative=False):
    if relative:
        return precisedelta(date.today() - value).capitalize()
    else:
        return naturaldate(value).capitalize()
