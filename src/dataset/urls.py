from django.conf.urls import url

import dataset.views as v

urlpatterns = [
    url(r'(?P<slug>[\w-]+)$', v.view_dataset, name='view_dataset'),
    url(r'$', v.search, name='search'),
]
