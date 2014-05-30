from base import settings

from smtplib import SMTP

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
  username = 'Bart'
  toAddress = 'bart@romgens.com'
  sendWelcomeMail(username, toAddress)

def sendMail(toAddress, fromAddress, subject, message):
#   header = "From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (fromAddress, toAddress, subject)
  msg = MIMEMultipart('alternative')
  msg['Subject'] = subject
  msg['From'] = fromAddress
  msg['To'] = toAddress
  
  msg.attach(MIMEText(message, 'html'))

  # Credentials (if needed)  
  username = 'computerautomatedremoteexchange'  
  password = settings.MAILPASSWORD  
  
  # The actual mail send  
  server = SMTP('smtp.webfaction.com:587')  
  server.starttls()  
  server.login(username, password)  
  server.sendmail(fromAddress, toAddress, msg.as_string())  
  server.quit()

def sendWelcomeMail(username, emailaddress):
  fromAddress = 'CARE <info@computerautomatedremoteexchange.com>'
  toAddress = emailaddress
  subject = 'Welcome to CARE!' 

  message = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Demystifying Email Design</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>

<body style="margin: 0; padding: 0;">
<p>Hi %s,</p>

<p>Welkom to CARE!</p>

<p>
You have created an account on CARE with the following information,
<br>
<br>
username: %s
<br>
email: %s
</p>

<p>
Log-in at <a href="http://www.computerautomatedremoteexchange.com">CARE</a> to get started. 
</p>

<p>
Have fun sharing,
<br>
CareBot
</p>

</body>

</html>
  """ % (username, username, emailaddress)

  sendMail(toAddress, fromAddress, subject, message)
  sendMail(fromAddress, fromAddress, subject, message)
  
  
if __name__ == "__main__":
  main()