from django.shortcuts import render
from login.authenticator import authenticated
from decisions.views import render_index

def render_login(request):
    """Render login"""
    if authenticated(request):
        return render_index(request)
    else:
        return render(request, 'login.html', {})

