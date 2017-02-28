from django import template

register = template.Library()


@register.filter
def filters_string(filters):
    """ Converts an dict of applied filters and returns a
    string ready for use in a URL. Should be first in the
    url so we can make sure we add the necessary & """
    if not filter:
        return ''
    return '&'.join('{}={}'.format(k, v) for k, v in filters.items()) + '&'
