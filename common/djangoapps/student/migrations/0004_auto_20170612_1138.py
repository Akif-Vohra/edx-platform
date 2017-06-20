# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20170612_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='salutation',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
