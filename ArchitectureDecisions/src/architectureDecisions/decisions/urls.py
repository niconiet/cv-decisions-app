from .views import *
from django.conf.urls import include, url

urlpatterns = [
    url(r'^index', render_index),
    url(r'^decision', decision),
    url(r'^writeComment/$', writeComment),
    url(r'^getComments/$', getComments),
    url(r'^getFullDecision/$', getFullDecision),
    url(r'^projects$', projects),
    url(r'^users$', users),
]
