from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^index', views.render_index),
    url(r'^decision', views.decision),
    url(r'^writeComment/$', views.writeComment),
    url(r'^getComments/$', views.getComments),
    url(r'^getFullDecision/$', views.getFullDecision),
    url(r'^projects$', views.projects),
    url(r'^users$', views.users),
]
