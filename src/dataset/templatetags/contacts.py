from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('dataset/includes/contacts.html')
def contacts(dataset):
    org = dataset.get('organisation')
    has_foi = org.get('foi_name') or org.get('foi_phone') \
        or org.get('foi_email') or org.get('foi_web')
    has_contact = org.get('contact_name') or org.get('contact_email') \
        or org.get('contact_phone')

    res = {
        'has_foi': has_foi,
        'has_contact': has_contact
    }
    res.update(org)
    return res
