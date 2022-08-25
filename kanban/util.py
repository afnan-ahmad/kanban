from datetime import datetime


def greeting_text(name):
    hour = datetime.now().hour
    if hour < 12:
        greeting = 'Good morning'
    elif 12 <= hour <= 17:
        greeting = 'Good afternoon'
    else:
        greeting = 'Good evening'

    return f'{greeting}, {name}'
