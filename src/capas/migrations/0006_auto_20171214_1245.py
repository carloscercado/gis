# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capas', '0005_auto_20171214_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]