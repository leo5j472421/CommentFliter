# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-08 05:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20161108_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='click_times',
            new_name='click',
        ),
    ]
