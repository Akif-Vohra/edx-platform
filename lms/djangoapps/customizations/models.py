from django.db import models
from student.models import CourseEnrollment


class SalesEmailHistory(models.Model):
    enrollment = models.ForeignKey(CourseEnrollment, unique=True , related_name="sales_emails")
    welcome_email_sent = models.BooleanField(default=False)
    motivational_email_sent = models.BooleanField(default=False)
    sales_funnel_email_sent = models.BooleanField(default=False)
    promote_lynx_account_email_sent = models.BooleanField(default=False)
    congratulation_email_sent = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0} {1}".format(self.enrollment.user, self.enrollment)