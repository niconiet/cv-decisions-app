from django.shortcuts import render,redirect
from .authenticator import authenticated


def render_login(request):
    """Render login"""
    if authenticated(request):
        return redirect('/index')
    else:
        return render(request, 'login.html', {})
