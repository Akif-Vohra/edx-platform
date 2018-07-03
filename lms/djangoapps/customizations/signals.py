from django.db.models.signals import post_save
from django.dispatch import receiver
from student.models import CourseEnrollment
from customizations.utils import send_sales_email, add_user_email_to_workflow, add_user_to_mailchimp
from customizations.models import SalesEmailHistory

import logging
AUDIT_LOG = logging.getLogger("audit")

@receiver(post_save, sender=CourseEnrollment, dispatch_uid="student_enrollment_created")
def send_welcome_email(sender, instance, **kwargs):
    if kwargs['created']:
        
        #Check if the course is the one we are looking for
        course_id = instance.course_id._to_string()
        if not course_id in ['LYNX+01+2017', 'LYNX+02+2018']:
            return

    	#Add user to mailchimp
    	try:
            add_user_to_mailchimp(instance, instance.course_id._to_string())
        except Exception as e:
            AUDIT_LOG.error("Error occurred while trying to add user to mailchimp list {0}".format(e))
        
        if course_id in "course-v1:LYNX+01+2017":
            add_user_email_to_workflow('HELLO_EMAIL', instance)

        elif course_id in "LYNX+02+2018":
            add_user_email_to_workflow('HELLO_EMAIL_SECOND_COURSE', instance)
        
        else:
            return

        sales_email_history, is_new = SalesEmailHistory.objects.get_or_create(enrollment=instance)
        sales_email_history.welcome_email_sent = True
        sales_email_history.save()
