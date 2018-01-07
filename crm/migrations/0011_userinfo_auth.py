# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-02 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('crm', '0010_auto_20180102_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='auth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.UserInfo', verbose_name='用户权限'),
        ),
    ]
