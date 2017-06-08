from django.db import models
from django.contrib.auth.models import User


class Gerencia(models.Model):
    name = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Nombre de la gerencia')
    gerencia_superior = models.ForeignKey("self",
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            help_text='Gerencia de nivel superior a la que pertenece')


class Departamento(models.Model):
    name = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Nombre del departamento')
    gerencia = models.ForeignKey(Gerencia, on_delete=models.CASCADE,
                            null=False,
                            blank=False,
                            help_text='Gerencia a la que pertenece')


class Responsible(models.Model):
    name = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Nombre del responsable')
    apellido = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Apellido del responsable')
    departamento = models.ForeignKey(Departamento,
                            on_delete=models.CASCADE,
                            null=False,
                            blank=False,
                            help_text='Deparamento al que pertenece')
    rol = models.CharField(max_length=200,
                            null=True,
                            blank=True,
                            help_text='Rol del responsable en la organizacion')


class Sponsor(models.Model):
    name = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Nombre del Sponsor')
    apellido = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Apellido del Sponsor')
    departamento = models.ForeignKey(Departamento,
                            on_delete=models.CASCADE,
                            null=False,
                            blank=False,
                            help_text='Deparamento al que pertenece')
    rol = models.CharField(max_length=200,
                            null=True,
                            blank=True,
                            help_text='Rol del sponsor en la organizacion')


class Project(models.Model):
    external_ID = models.CharField(max_length=200,
                            null=True,
                            blank=True,
                            help_text='Identificador externo del proyecto, por ejemplo el usado en el sistema de gestion de proyectos')
    name = models.CharField(max_length=200,
                            null=False,
                            blank=False,
                            help_text='Nombre del proyecto')
    sponsor = models.ForeignKey(Sponsor,
                            on_delete=models.CASCADE,
                            null = False,
                            help_text='Sponsor del proyecto')
    responsible = models.ForeignKey(Responsible,
                            on_delete=models.CASCADE,
                            null=False,
                            help_text='Responsable en la organizacion')
    main_architect = models.ForeignKey(User,
                            on_delete=models.SET_NULL,
                            null=True,
                            help_text='Arquitecto asignado al proyecto')