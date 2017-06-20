# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20170612_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
