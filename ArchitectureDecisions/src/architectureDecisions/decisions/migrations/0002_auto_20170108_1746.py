# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('decisions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='related_decision',
            field=models.ForeignKey(blank=True, help_text='Relacion con otra decision que influyo en la actual', null=True, on_delete=django.db.models.deletion.CASCADE, to='decisions.Decision'),
        ),
    ]
