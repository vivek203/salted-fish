# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kelp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpawningStreamLength',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incubation_time', models.FloatField()),
                ('stream_length', models.FloatField()),
                ('actual_length', models.FloatField()),
                ('station_id', models.CharField(max_length=100)),
                ('station_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='dischargedata',
            name='velocity',
            field=models.FloatField(default=0),
        ),
    ]
