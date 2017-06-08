from django.db import models
from django.contrib.auth.models import User
from projects.models import *

SOLUTION = 'SOL'
APPLICATION = 'APP'
INTEGRATION = 'INT'
DATA = 'DAT'
INFRASTRUCTURE = 'INF'

ARCHITECTURE_DOMAINS_CHOICES = (
    (SOLUTION, 'Soluciones'),
    (APPLICATION, 'Aplicaciones'),
    (INTEGRATION, 'Integraciones'),
    (DATA, 'Datos'),
    (INFRASTRUCTURE, 'Infraestructura')
)

DECISION_STATES_CHOICES = (
    ('Tomada', 'Tomada'),
    ('Pendiente','Pendiente')
)


class Decision(models.Model):
    affected_project = models.ForeignKey(Project,
                            on_delete=models.CASCADE,
                            null=False,
                            help_text='Proyecto afectado por la decision')
    decisor = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            null=False,
                            help_text='Arquitecto que toma la decision sobre un proyecto')
    domain = models.CharField(max_length=3,
                            choices=ARCHITECTURE_DOMAINS_CHOICES,
                            default=SOLUTION,
                            help_text='Dominio de arquitectura impactado por la decision')
    notice_date = models.DateField(help_text='Fecha en la que la decision es tomada')
    effective_date = models.DateField(null=True,
                            blank=True,
                            help_text='Fecha en la que la decision se hace efectiva')
    decision_details = models.CharField(max_length=1000,
                            null=False,
                            blank=False,
                            help_text='Detalle de la decision que se toma')
    basis = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            help_text='Fundamentos de la decision')
    scope = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            help_text='Alcance de la decision, a nivel organizacional o entorno de ejecucion')
    impact = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            help_text='Impacto que tiene la decision. Pueden ser componentes, areas organizacionales o proyectos, por ejemplo')
    alternatives = models.CharField(max_length=500,
                            null=True,
                            blank=True,
                            help_text='Alternativas que fueron evaluadas para tomar la decision')
    related_decision = models.ForeignKey("self",
                            null=True,
                            blank=True,
                            help_text='Relacion con otra decision que influyo en la actual')
    decision_state = models.CharField(max_length=15,
                            choices=DECISION_STATES_CHOICES,
                            default='Tomada',
                            help_text='Estado de la decision')

class Comment(models.Model):
    affected_decision = models.ForeignKey(Decision,
                            null=False,
                            help_text='Decision afectada por el comentario')
    comment_date = models.DateField(auto_now=True,
                            help_text='Fecha que se realiza el comentario')
    commenter = models.CharField(max_length=20,
                            help_text='Persona que realizo el comentario (o anonimo)')
    comment = models.CharField(max_length=200,
                            help_text='Comentario sobre la decision o sobre otro comentario')
    reply_to = models.PositiveSmallIntegerField(blank=True,
                            null=True,
                            help_text='Comentario que responde a otro')