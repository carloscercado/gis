# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 00:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capas', '0006_auto_20171214_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capas',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capas', to='capas.Categoria'),
        ),
    ]
