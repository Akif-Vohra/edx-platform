"""
Script for importing courseware from XML format
"""
from optparse import make_option
from random import randint, uniform

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django_comment_common.utils import (seed_permissions_roles,
                                         are_permissions_roles_seeded)
from xmodule.modulestore.xml_importer import import_course_from_xml
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.django import modulestore
from xmodule.contentstore.django import contentstore
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.models import CourseEnrollment
from opaque_keys.edx.keys import CourseKey
from courseware.grades import iterate_grades_for
from courseware.courses import get_course
from django.conf import settings
from customizations.models import SalesEmailHistory
from customizations.utils import send_sales_email, add_user_to_mailchimp, add_user_email_to_workflow

import logging
import os


class Command(BaseCommand):
    """
    Import the specified data directory into the default ModuleStore
    """
    help = 'Import the specified data directory into the default ModuleStore'

    option_list = BaseCommand.option_list + (
        make_option('--nostatic',
                    action='store_true',
                    help='Skip import of static content'),
    )

    def handle(self, *args, **options):

        try:
            course_key = CourseKey.from_string('course-v1:LYNX+001+2016')
        except InvalidKeyError:
            course_key = SlashSeparatedCourseKey.from_deprecated_string('course-v1:LYNX+001+2016')

        course = get_course(course_key)

        enrollments = CourseEnrollment.objects.filter(course_id=course.id, is_active=True)
        enrolled_students = CourseEnrollment.objects.users_enrolled_in(course_id=course.id)

        email_dict = dict(motivational_email=[],
                          sales_funnel_email=[],
                          promote_lynx_account_email=[],
                          congratulation_email=[])

        for student, gradeset, err_msg in iterate_grades_for(course.id, enrolled_students):
            if gradeset:
                try:
                    enrollment = enrollments.filter(user=student)[0]
                except Exception as e:
                    print e
                    continue
                
                # First check for welcome email
                sales_email_history, is_new = SalesEmailHistory.objects.get_or_create(enrollment=enrollment)

                # Get User Enrollments
                user = enrollment.user

                enrolled_at = enrollment.created

                time_diff = (timezone.now() - enrolled_at).days
                percent = gradeset['percent']

                print "Student with email {0} has been enrolled for {1} days and has achieved {2} percent so far".format(
                    user.email, time_diff, percent)

                if (time_diff >= 7) and (time_diff < 14) and percent < 0.70:
                    if not sales_email_history.motivational_email_sent:
                        add_user_email_to_workflow('MOTIVATIONAL_EMAIL', enrollment)
                        sales_email_history.motivational_email_sent = True

                elif time_diff >= 14 and percent < 0.80:
                    if percent < 0.30:
                        if not sales_email_history.sales_funnel_email_sent:
                            add_user_email_to_workflow('LESS_THAN_30', enrollment)
                            sales_email_history.sales_funnel_email_sent = True

                    elif (percent >= 0.30) and (percent < 0.50):
                        if not sales_email_history.promote_lynx_account_email_sent:
                            add_user_email_to_workflow('LESS_THAN_50', enrollment)
                            sales_email_history.promote_lynx_account_email_sent = True

                if percent >= 0.80:
                    if not sales_email_history.congratulation_email_sent:
                        add_user_email_to_workflow('MORE_THAN_80', enrollment)
                        sales_email_history.congratulation_email_sent = True

                else:
                    print "No conditions matched"

                sales_email_history.save()
