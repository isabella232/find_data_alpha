from django.conf.urls import url

import stats.views as v

urlpatterns = [
    url(r'^$', v.top, name='top'),
]
