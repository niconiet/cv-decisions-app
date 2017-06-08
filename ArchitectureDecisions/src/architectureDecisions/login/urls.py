from login.views import *
from django.conf.urls import include, url
from login.authenticator import *

urlpatterns = [
    url(r'^login$', render_login),
    url(r'^logout$', logout),
    url(r'^authenticate$', authenticate),
    url(r'^authorization$', authorization),
]