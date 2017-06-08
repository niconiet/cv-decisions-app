from . import views, authenticator
from django.conf.urls import include, url

urlpatterns = [
    url(r'^login$', views.render_login),
    url(r'^logout$', authenticator.logout),
    url(r'^authenticate$', authenticator.authenticate),
    url(r'^authorization$', authenticator.authorization),
]