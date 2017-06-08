# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gerencia',
            name='gerencia_superior',
            field=models.ForeignKey(blank=True, help_text='Gerencia de nivel superior a la que pertenece', null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Gerencia'),
        ),
    ]
