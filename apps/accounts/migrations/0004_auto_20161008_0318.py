# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-08 03:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Chapter', to='accounts.Course'),
        ),
        migrations.AddField(
            model_name='flashcard',
            name='chapter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='flashcards', to='accounts.Chapter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.ManyToManyField(related_name='courses', to='accounts.Course'),
        ),
        migrations.AddField(
            model_name='user',
            name='teaches',
            field=models.ManyToManyField(related_name='teaches', to='accounts.Course'),
        ),
    ]