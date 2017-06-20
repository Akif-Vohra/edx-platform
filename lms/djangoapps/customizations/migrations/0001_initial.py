# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20151208_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesEmailHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('welcome_email_sent', models.BooleanField(default=False)),
                ('motivational_email_sent', models.BooleanField(default=False)),
                ('sales_funnel_email', models.BooleanField(default=False)),
                ('promote_lynx_account_email', models.BooleanField(default=False)),
                ('congratulation_email', models.BooleanField(default=False)),
                ('enrollment', models.ForeignKey(related_name='sales_emails', to='student.CourseEnrollment')),
            ],
        ),
    ]
