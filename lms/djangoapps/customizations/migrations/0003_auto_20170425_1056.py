# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0002_auto_20170425_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesemailhistory',
            name='congratulation_email',
        ),
        migrations.RemoveField(
            model_name='salesemailhistory',
            name='promote_lynx_account_email',
        ),
        migrations.RemoveField(
            model_name='salesemailhistory',
            name='sales_funnel_email',
        ),
        migrations.AddField(
            model_name='salesemailhistory',
            name='congratulation_email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salesemailhistory',
            name='promote_lynx_account_email_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salesemailhistory',
            name='sales_funnel_email_sent',
            field=models.BooleanField(default=False),
        ),
    ]
