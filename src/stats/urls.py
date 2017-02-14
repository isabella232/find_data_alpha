from django.conf.urls import url

import stats.views as v

urlpatterns = [
    url(r'^$', v.top, name='top'),
    url(r'^(?P<organisation_id>[0-9a-z-]+)$', v.top_organisation, name='top_organisation'),
]
