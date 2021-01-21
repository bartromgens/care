import os
import threading
import logging

from django.core.mail import send_mail

from care import settings

module_dir = os.path.dirname(__file__)  # get current directory
logger = logging.getLogger(__name__)


def send_html_mail(email_to, email_from, subject, message):
    send_mail(subject, message, email_from, [email_to])


def send_transaction_history(username, emailaddress, transactionTable, transactionRealTable, startDate, endDate):
    email_from = 'Care <info@computerautomatedremoteexchange.com>'
    email_to = emailaddress
    subject = 'Care transaction history'
    logging.info('send_transaction_history from: ' + str(email_from) + ' to: ' + str(email_to))

    message = ''
    with open( os.path.join(module_dir, 'transactionhistorymail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% transactionTable %}', transactionTable)
    message = message.replace('{% transactionRealTable %}', transactionRealTable)
    message = message.replace('{% username %}', username)
    message = message.replace('{% startDate %}', startDate.strftime('%d %B %Y') )
    message = message.replace('{% endDate %}', endDate.strftime('%d %B %Y') )

    send_html_mail(email_to, email_from, subject, message)


def send_welcome_email(username, emailaddress):
    email_from = 'Care <info@computerautomatedremoteexchange.com>'
    email_to = emailaddress
    subject = 'Welcome to Care!'
    logging.debug('send_welcome_email from: ' + str(email_from) + ' to: ' + str(email_to))

    message = ''

    with open( os.path.join(module_dir, 'welcomemail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% username %}', username)
    message = message.replace('{% email %}', emailaddress)

    send_html_mail(email_to, email_from, subject, message)


def send_invite_email(username_from, username_to, group_name, emailaddress):
    email_from = 'Care <info@computerautomatedremoteexchange.com>'
    email_to = emailaddress
    subject = 'New invitation'

    logging.debug('send_invite_email from: ' + str(email_from) + ' to: ' + str(email_to))

    message = ''
    with open( os.path.join(module_dir, 'invitemail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% usernameTo %}', username_to)
    message = message.replace('{% usernameFrom %}', username_from)
    message = message.replace('{% groupName %}', group_name)

    send_html_mail(email_to, email_from, subject, message)


def send_low_balance_reminder(user, group):
    email_from = 'Care <info@computerautomatedremoteexchange.com>'
    email_to = user.email
    subject = 'Low balance in ' + group.name + ''

    logging.debug('send_low_balance_reminder from: ' + str(email_from) + ' to: ' + str(email_to))

    message = ''
    with open( os.path.join(module_dir, 'balancereminder.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    from care.userprofile.models import UserProfile
    userprofile = UserProfile.objects.get(user=user)

    message = message.replace('{% username %}', userprofile.displayname)
    message = message.replace('{% group_name %}', group.name)
    message = message.replace('{% group_user_balance %}', str('%.2f' % UserProfile.get_balance(group.id, userprofile.id)))
    message = message.replace('{% lower_limit %}', str(group.settings.notification_lower_limit))

    send_html_mail(email_to, email_from, subject, message)
