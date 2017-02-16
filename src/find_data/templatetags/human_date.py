import datetime
import dateutil.parser

from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter('human_date')
def human_date(date_string, format):
    parsed_date = dateutil.parser.parse(date_string)
    return datetime.date.strftime(parsed_date, format)
