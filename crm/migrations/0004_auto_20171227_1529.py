# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 07:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20171227_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='bb',
        ),
        migrations.AddField(
            model_name='customer',
            name='recv_date',
            field=models.DateField(blank=True, null=True, verbose_name='接客日期'),
        ),
    ]