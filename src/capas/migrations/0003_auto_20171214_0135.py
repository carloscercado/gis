# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capas', '0002_atributos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atributos',
            name='capa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atributos', to='capas.Capas'),
        ),
        migrations.AlterField(
            model_name='atributos',
            name='descripcion',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='atributos',
            name='tipo',
            field=models.CharField(choices=[('Point', 'Point'), ('Polygon', 'Polygon'), ('LineString', 'LineString'), ('Text', 'Text'), ('Int', 'Int'), ('Float', 'Float'), ('MultiPolygon', 'MultiPolygon'), ('MultiLineString', 'MultiLineString')], max_length=30),
        ),
    ]