#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from .models import MailAccount
from django.conf import settings


class ReportSettings:
    to_list = []
    #if not settings.DEBUG:
    #    cursor = MailAccount.objects.all()
    #    for element in cursor:
    #        to_list.append(element.mail)
    #else:
    #    to_list = ["nrnieto@cablevision.com.ar"]
    to_list = ["nrnieto@cablevision.com.ar"]
    db_path = settings.DATABASES['default']['NAME']
    subtitle = 'Reporte de decisiones tomadas al ' + str(datetime.date.today().strftime('%d-%m-%Y'))
    title = 'Arquitectura de Sistemas'
    body_text = "Estimados, adjunto encontrarán el listado de decisiones actualizado a la fecha.\nPuede consultar y comentar estas decisiones en http://sisarqdec.corp.cablevision.com.ar"
    subject = "Arquitectura IT: Reporte semanal de decisiones"
    from_addr = "sisarq@cablevision.com.ar"
    attachment_filename = 'reporte'

