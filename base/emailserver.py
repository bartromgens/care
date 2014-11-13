from base import settings

from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import threading

import os
module_dir = os.path.dirname(__file__)  # get current directory

import logging
logger = logging.getLogger(__name__)


def main():
    username = 'Bart'
    usernameTo = 'Jaap'
    toAddress = 'bart@romgens.com'
#   send_welcome_email(username, toAddress)
    send_invite_email(username, usernameTo, "testgroup", toAddress)
    logger.info("main() end")


class EmailThread(threading.Thread):
    def __init__(self, toAddress, fromAddress, subject, message):
        self.toAddress = toAddress
        self.fromAddress = fromAddress
        self.subject = subject
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.fromAddress
        msg['To'] = self.toAddress

        msg.attach(MIMEText(self.message, 'html'))

        # Credentials (if needed)
        username = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD

        # The actual mail send
        server = SMTP( settings.EMAIL_HOST + ':' + str(settings.EMAIL_PORT) )
        server.starttls()
        server.login(username, password)
        server.sendmail(self.fromAddress, self.toAddress, msg.as_string())
        server.quit()
        logger.info("finished sending mail")

def send_html_mail(toAddress, fromAddress, subject, message):
    EmailThread(toAddress, fromAddress, subject, message).start()


def send_transaction_history(username, emailaddress, transactionTable, transactionRealTable, startDate, endDate):
    fromAddress = 'Care <info@computerautomatedremoteexchange.com>'
    toAddress = emailaddress
    subject = 'Care transaction history'
    logging.info('send_transaction_history from: ' + str(fromAddress) + ' to: ' + str(toAddress))

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

#   with open('test.hml', 'w') as fileout:
#     fileout.write(message)
    send_html_mail(toAddress, fromAddress, subject, message)


def send_welcome_email(username, emailaddress):
    fromAddress = 'Care <info@computerautomatedremoteexchange.com>'
    toAddress = emailaddress
    subject = 'Welcome to Care!'
    logging.debug('send_welcome_email from: ' + str(fromAddress) + ' to: ' + str(toAddress))

    message = ''

    with open( os.path.join(module_dir, 'welcomemail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% username %}', username)
    message = message.replace('{% email %}', emailaddress)

    send_html_mail(toAddress, fromAddress, subject, message)


def send_invite_email(usernameFrom, usernameTo, groupName, emailaddress):
    fromAddress = 'Care <info@computerautomatedremoteexchange.com>'
    toAddress = emailaddress
    subject = 'New invitation'

    logging.debug('send_invite_email from: ' + str(fromAddress) + ' to: ' + str(toAddress))

    message = ''

    with open( os.path.join(module_dir, 'invitemail.html'), 'r' ) as filein:
        data = filein.readlines()
        for row in data:
            message += row

    message = message.replace('{% usernameTo %}', usernameTo)
    message = message.replace('{% usernameFrom %}', usernameFrom)
    message = message.replace('{% groupName %}', groupName)

    send_html_mail(toAddress, fromAddress, subject, message)


if __name__ == "__main__":
    main()
