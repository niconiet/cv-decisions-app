# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre del departamento', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Gerencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre de la gerencia', max_length=200)),
                ('gerencia_superior', models.ForeignKey(help_text='Gerencia de nivel superior a la que pertenece', null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Gerencia')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_ID', models.CharField(blank=True, help_text='Identificador externo del proyecto, por ejemplo el usado en el sistema de gestion de proyectos', max_length=200, null=True)),
                ('name', models.CharField(help_text='Nombre del proyecto', max_length=200)),
                ('main_architect', models.ForeignKey(help_text='Arquitecto asignado al proyecto', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Responsible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre del responsable', max_length=200)),
                ('apellido', models.CharField(help_text='Apellido del responsable', max_length=200)),
                ('rol', models.CharField(blank=True, help_text='Rol del responsable en la organizacion', max_length=200, null=True)),
                ('departamento', models.ForeignKey(help_text='Deparamento al que pertenece', on_delete=django.db.models.deletion.CASCADE, to='projects.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nombre del Sponsor', max_length=200)),
                ('apellido', models.CharField(help_text='Apellido del Sponsor', max_length=200)),
                ('rol', models.CharField(blank=True, help_text='Rol del sponsor en la organizacion', max_length=200, null=True)),
                ('departamento', models.ForeignKey(help_text='Deparamento al que pertenece', on_delete=django.db.models.deletion.CASCADE, to='projects.Departamento')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='responsible',
            field=models.ForeignKey(help_text='Responsable en la organizacion', on_delete=django.db.models.deletion.CASCADE, to='projects.Responsible'),
        ),
        migrations.AddField(
            model_name='project',
            name='sponsor',
            field=models.ForeignKey(help_text='Sponsor del proyecto', on_delete=django.db.models.deletion.CASCADE, to='projects.Sponsor'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='gerencia',
            field=models.ForeignKey(help_text='Gerencia a la que pertenece', on_delete=django.db.models.deletion.CASCADE, to='projects.Gerencia'),
        ),
    ]
