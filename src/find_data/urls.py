
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    url(r'^download/(?P<dataset_id>[0-9a-z-]+)/(?P<resource_id>[0-9a-z-]+)$',
        views.download, name='download'),
    url(r'^dataset/', include('dataset.urls')),
]
