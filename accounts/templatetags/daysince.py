from django import template
import datetime

register = template.Library()

def dayssince(value):
    "Returns number of days between today and value."
    today = datetime.date.today()
    diff  = today - value
    if diff.days > 7:
        return u'more than a week ago'
    elif diff.days > 1:
        return u'in this week'
    elif diff.days == 1:
        return u'yesterday'
    elif diff.days == 0:
        return u'today'
    else:
        # Date is in the future; return formatted date.
        return value.strftime("%B %d, %Y")

register.filter('dayssince', dayssince)