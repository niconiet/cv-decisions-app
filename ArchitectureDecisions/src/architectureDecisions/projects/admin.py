from django.contrib import admin
from .models import Gerencia, Departamento, Responsible, Sponsor, Project

admin.site.register(Gerencia)
admin.site.register(Departamento)
admin.site.register(Responsible)
admin.site.register(Sponsor)
admin.site.register(Project)
