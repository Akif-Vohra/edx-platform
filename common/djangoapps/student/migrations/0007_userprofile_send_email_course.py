# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20170620_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='send_email_course',
            field=models.BooleanField(default=False),
        ),
    ]
