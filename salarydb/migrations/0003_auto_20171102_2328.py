# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-03 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salarydb', '0002_auto_20171102_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]
