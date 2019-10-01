# Use datetime if not localizing timezones
import datetime
import time
# Otherwise use timezone
from django.utils import timezone

from django import template

register = template.Library()

@register.filter("hours_ago")

def hours_ago(time, hours):
    time = time.replace(tzinfo=None)
    #return time + datetime.timedelta(hours=hours) < timezone.now() # or timezone.now() if your time is offset-aware
    return time + datetime.timedelta(hours=hours) < datetime.datetime.now() # or timezone.now() if your time is offset-aware
    '''if(time is None):
        return False
    else:
        return time + datetime.timedelta(24) < timezone.now()'''

@register.filter("humanizeTimeDiff")
def humanizeTimeDiff(timestamp = None):
    """
    Returns a humanized string representing time difference
    between now() and the input timestamp.

    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """
    #if(timestamp is None):
        #return ''
    #timeDiff = timezone.now() - timestamp
    timestamp = timestamp.replace(tzinfo=None)
    timeDiff = datetime.datetime.now() - timestamp

    daySecs = 86400
    hourSecs = 3600
    minSecs = 60
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60

    str = ""
    tStr = ""
    if hours > 0:
        if hours == 1:  tStr = "hour"
        else:           tStr = "hours"
        str = str + "%s %s" %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = "min"
        else:           tStr = "mins"
        str = str + "%s %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "sec"
        else:           tStr = "secs"
        str = str + "%s %s" %(seconds, tStr)
        return str
    else:
        return None

@register.filter("increase_self")
def increase_self(num_value):
    return num_value + 1

@register.filter("get_first_word")
def get_first_word(word):
    els = word.split(' ')
    return els[0]

@register.filter(name='get_var_arr')
def get_var_arr(d, k):
    return d.get(k, None)\

@register.filter(name='change_str_to_date')
def change_str_to_date(d):
    return datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    #today = datetime.datetime.strptime(article_published_date, "%d-%m-%Y")
    #return time.strftime("%Y-%m-%d %H:%M:%S", d)