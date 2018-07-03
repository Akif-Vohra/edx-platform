from django.conf import settings
import mandrill
from mailchimp3 import MailChimp

API_KEY = settings.EMAIL_HOST_PASSWORD

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_USER_NAME = settings.MAILCHIMP_USER_NAME
MAILCHIMP_OPTION_COURSE_LIST_ID = settings.MAILCHIMP_OPTION_COURSE_LIST_ID
MAILCHIMP_OPTION_SECOND_COURSE_LIST_ID = settings.MAILCHIMP_OPTION_SECOND_COURSE_LIST_ID

mail_chimp_client = MailChimp(MAILCHIMP_USER_NAME, MAILCHIMP_API_KEY)

import logging
AUDIT_LOG = logging.getLogger("audit")

EMAIL_TYPE_TO_WORKFLOW_EMAIL_ID = settings.EMAIL_TYPE_TO_WORKFLOW_EMAIL_ID

def send_mail_transactional(template_name, email_to, global_merge_vars):
    mandrill_client = mandrill.Mandrill(API_KEY)
    message = {
        'to': [],
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})

    for k, v in global_merge_vars.iteritems():
        message['global_merge_vars'].append(
            {'name': k, 'content': v}
        )
    mandrill_client.messages.send_template(template_name, [], message)


def send_sales_email(template_name, enrollment):

    user = enrollment.user

    FNAME = user.profile.first_name
    LNAME = user.profile.last_name
    TITLE = user.profile.title

    if user.profile.gender == 'm':
        SALUTATION = 'Herr'
    elif user.profile.gender == 'f':
        SALUTATION = 'Frau'
    else:
        SALUTATION = ''
    
    global_merge_vars = dict(FNAME=FNAME, LNAME=LNAME, SALUTATION=SALUTATION, TITLE=TITLE)
    send_mail_transactional(template_name, [enrollment.user.email], global_merge_vars)


def get_option_kurse_list():
    list_id = None
    mailchimp_lists = mail_chimp_client.lists.all(get_all=True, fields="lists.id,lists.web_id,lists.name")
    for mailchimp_list in mailchimp_lists['lists']:
        if mailchimp_list['name'] == u'LYNX Online-Training Optionen Basiskurs 1':
            list_id = mailchimp_list['id']

    return list_id

def add_user_to_mailchimp(enrollment, course_id):

    if course_id in "LYNX+01+2017":
        list_id = MAILCHIMP_OPTION_COURSE_LIST_ID #This should never change.. Unless mailchimp goes crazy

    elif course_id in "LYNX+02+2018":
        list_id = MAILCHIMP_OPTION_SECOND_COURSE_LIST_ID

    else:
        return

    print "Adding {0} to list {1}".format( enrollment.user, list_id )
    user = enrollment.user
    FNAME = user.profile.first_name
    LNAME = user.profile.last_name
    TITLE = user.profile.title

    if user.profile.gender == 'm':
        SALUTATION = 'Herr'
    elif user.profile.gender == 'f':
        SALUTATION = 'Frau'
    else:
        SALUTATION = ''

    global_merge_vars = dict(FNAME=FNAME, LNAME=LNAME, SALUTATION=SALUTATION, TITLE=TITLE if TITLE else '')
    print global_merge_vars
    print list_id
    print user.email
    try:
        mail_chimp_client.lists.members.create(list_id, {
            'email_address': user.email,
            'status': 'subscribed',
            'merge_fields': global_merge_vars
            })
    except Exception as e:
        AUDIT_LOG.error("Error while adding user {0} in mailchimp list {2}".format(user.email, e))

def add_user_email_to_workflow(email_type, enrollment):
    print "sending {0} to user {1}".format(email_type, enrollment.user.email)
    try:
        email_address = enrollment.user.email
        workflow_id = EMAIL_TYPE_TO_WORKFLOW_EMAIL_ID[email_type]['workflow_id']
        workflow_email_id = EMAIL_TYPE_TO_WORKFLOW_EMAIL_ID[email_type]['workflow_email_id']
        mail_chimp_client.automations.emails.queues.create(workflow_id, workflow_email_id, {
            'email_address' : email_address
            })
    except Exception as e:
        AUDIT_LOG.error("Error adding user to workflow {0} {1} {2}".format(email_type, enrollment, e))


