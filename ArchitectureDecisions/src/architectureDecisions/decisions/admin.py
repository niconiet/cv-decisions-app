from django.contrib import admin
from .models import Decision
from .models import Comment

admin.site.register(Decision)
admin.site.register(Comment)