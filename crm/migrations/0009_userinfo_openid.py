# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-28 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20171227_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='openid',
            field=models.CharField(default=2, max_length=64, verbose_name='微信唯一id'),
            preserve_default=False,
        ),
    ]