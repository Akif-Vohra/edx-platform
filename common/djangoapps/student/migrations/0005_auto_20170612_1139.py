# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_auto_20170612_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='salutation',
            new_name='title',
        ),
    ]
