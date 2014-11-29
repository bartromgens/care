from base import settings

from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import threading

import os
module_dir = os.path.dirname(__file__)  # get current directory

import logging
logger = logging.getLogger(__name__)


class EmailThread(threading.Thread):
    def __init__(self, email_to, email_from, subject, message):
        self.email_to = email_to
        self.email_from = email_from
        self.subject = subject
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.email_from
        msg['To'] = self.email_to

        msg.attach(MIMEText(self.message, 'html'))

        # Credentials (if needed)
        username = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        # The actual mail send
        server = SMTP( settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT) )
        server.starttls()
        server.login(username, password)
        server.sendmail(self.email_from, self.email_to, msg.as_string())
        server.quit()
        logger.info("finished sending mail")

def send_html_mail(email_to, email_from, subject, message):
    EmailThread(email_to, email_from, subject, message).start()


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


def send_invite_email(usernameFrom, usernameTo, groupName, emailaddress):
    email_from = 'Care <info@computerautomatedremoteexchange.com>'
    email_to = emailaddress
    subject = 'New invitation'

    logging.debug('send_invite_email from: ' + str(email_from) + ' to: ' + str(email_to))

    message = ''
    with open( os.path.join(module_dir, 'invitemail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% usernameTo %}', usernameTo)
    message = message.replace('{% usernameFrom %}', usernameFrom)
    message = message.replace('{% groupName %}', groupName)

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

    from userprofile.models import UserProfile
    userprofile = UserProfile.objects.get(user=user)

    message = message.replace('{% username %}', userprofile.displayname)
    message = message.replace('{% group_name %}', group.name)
    message = message.replace('{% group_user_balance %}', str(UserProfile.get_balance(group.id, userprofile.id) ))
    message = message.replace('{% lower_limit %}', str(group.settings.notification_lower_limit))

    send_html_mail(email_to, email_from, subject, message)
    