# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-18 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=20)),
                ('video_id', models.CharField(max_length=20)),
                ('all_comments', models.DecimalField(decimal_places=0, max_digits=5)),
                ('machine_num', models.DecimalField(decimal_places=0, max_digits=5)),
            ],
        ),
    ]
