# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesemailhistory',
            name='enrollment',
            field=models.ForeignKey(related_name='sales_emails', to='student.CourseEnrollment', unique=True),
        ),
    ]
