from django.conf import settings
import mandrill
from mailchimp3 import MailChimp

API_KEY = settings.EMAIL_HOST_PASSWORD

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_USER_NAME = settings.MAILCHIMP_USER_NAME
MAILCHIMP_OPTION_COURSE_LIST_ID = settings.MAILCHIMP_OPTION_COURSE_LIST_ID

mail_chimp_client = MailChimp(MAILCHIMP_USER_NAME, MAILCHIMP_API_KEY)

EMAIL_TYPE_TO_WORKFLOW_EMAIL_ID = {
    
    'HELLO_EMAIL' : dict(workflow_id='09d0d88691', workflow_email_id='4067917b88'),
    'MOTIVATIONAL_EMAIL' : dict(workflow_id='09d0d88691', workflow_email_id='6040f5e43e'),
    'LESS_THAN_50' : dict(workflow_id='09d0d88691', workflow_email_id='af9c43bed0'),
    'MORE_THAN_80' : dict(workflow_id='09d0d88691', workflow_email_id='0bdd6c6e00'),
    #This ones different. Please note workflow_id
    'LESS_THAN_30' : dict(workflow_id='355eed901a', workflow_email_id='5500d7cc61'),
}

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

def add_user_to_mailchimp(enrollment):
    list_id = MAILCHIMP_OPTION_COURSE_LIST_ID #This should never change.. Unless mailchimp goes crazy
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

    mail_chimp_client.lists.members.create(list_id, {
        'email_address': user.email,
        'status': 'subscribed',
        'merge_fields': global_merge_vars
        })

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
        print "Because this is Graceful!"


