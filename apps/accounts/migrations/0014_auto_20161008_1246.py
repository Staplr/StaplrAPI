# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-08 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20161008_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='class_identifier',
            field=models.CharField(default='6dd59ba', max_length=7, unique=True),
        ),
    ]
