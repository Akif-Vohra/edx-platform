from django.db.models.signals import post_save
from django.dispatch import receiver
from student.models import CourseEnrollment
from customizations.utils import send_sales_email, add_user_email_to_workflow, add_user_to_mailchimp
from customizations.models import SalesEmailHistory


@receiver(post_save, sender=CourseEnrollment, dispatch_uid="student_enrollment_created")
def send_welcome_email(sender, instance, **kwargs):
    if kwargs['created']:
    	#Add user to mailchimp
    	try:
        	add_user_to_mailchimp(instance)
        except Exception as e:
        	print e

        #When that is done. Trigger first email
        add_user_email_to_workflow('HELLO_EMAIL', instance)

        sales_email_history, is_new = SalesEmailHistory.objects.get_or_create(enrollment=instance)
        sales_email_history.welcome_email_sent = True
        sales_email_history.save()
