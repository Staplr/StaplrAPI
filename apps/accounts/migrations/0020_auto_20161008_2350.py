# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-08 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20161008_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='class_identifier',
            field=models.CharField(default='07bc41c', max_length=7, unique=True),
        ),
    ]