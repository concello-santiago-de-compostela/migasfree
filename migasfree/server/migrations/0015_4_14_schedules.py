# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-04-04 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_4_14_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledelay',
            name='schedule',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='delays',
                to='server.Schedule',
                verbose_name='schedule'
            ),
        ),
    ]
