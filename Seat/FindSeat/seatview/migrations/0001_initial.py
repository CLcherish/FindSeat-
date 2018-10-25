# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('pwd', models.CharField(max_length=20)),
                ('uphone', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seatid', models.CharField(max_length=10)),
                ('status', models.CharField(default=b'free', max_length=20)),
                ('customername', models.CharField(max_length=20)),
            ],
        ),
    ]
