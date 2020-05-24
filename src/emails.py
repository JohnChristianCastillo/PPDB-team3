import smtplib
import imaplib

global sender


def send_email_signedup(email):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'Welcome to campus carpool!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "Your account on Campus Carpool was successfully created! You can now log in, find rides, create rides,"
    body += " and edit your account at team3.ppdb.me!\n"
    body += "If you no longer want to receive these emails, you can turn it off in 'Edit account'.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_newpassenger(email, passenger_name, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A passenger has joined your ride!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "A new passenger, " + passenger_name + ", has joined your ride on " + depart_time + " to " + destination + "!\n"
    body += "To view this passenger's profile, go to 'My rides' and click on their profile picture. \n"
    body += "To delete your ride, go to 'My rides' and click 'Delete ride'.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_deletedride(email, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A ride you joined has been deleted.'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "A ride you recently joined to " + destination + " on " + depart_time + " has been deleted by the driver.\n"
    body += "If you still need a ride, we suggest joining a new one.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_passengercancelled(email, passenger_name, depart_time, destination):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'A passenger has cancelled their involvement in your ride.'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "Your passenger, " + passenger_name + ", has cancelled your ride on " + depart_time + " to " + destination + ".\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()

def send_email_review(email, review_writer):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'Someone wrote a review about you!'

    recipient = email

    headers = ["From: " + send_from,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    # "Content-Type: text/html"]
    # to use html in body
    headers = "\r\n".join(headers)
    body = "User " + review_writer + " has written a review about you. You can see your reviews and rating on your account page.\n"
    body += "Thank you for using Campus Carpool!"

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, headers + "\r\n\r\n" + body)
    session.quit()


def send_email_calendar(email, ics_content):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587

    send_from = 'campus.carpool.ua@gmail.com'
    password = 'campuscarpool2020'
    subject = 'Your calendar events are here!'

    recipient = email

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    msg = MIMEMultipart()
    msg['Subject'] = subject,
    msg['From'] = send_from,
    msg['To'] = recipient

    body = "Hi there! \n\n"
    body += "You requested calendar events of your rides, so here they are!\n\n"
    body += "How does it work?\n"
    body += "In mailing apps like Outlook there is a possibility to click on the calendar symbol on the attached " \
            "ics file.\n "
    body += "Other apps like Gmail require some more action. For Google Calendar, this is wat you need to do:\n"
    body += "\t 1) Open Google Calendar\n"
    body += "\t 2) Go to settings\n"
    body += "\t 3) Click import and export\n"
    body += "\t 4) Choose import\n"
    body += "\t 5) Download the file attached to this email\n"
    body += "\t 6) Upload this file on Google calendar\n"
    body += "\t 7) Hit 'import' and you're al done!\n"

    msg.attach(MIMEText(body))

    part = MIMEBase('text', 'calendar', **{'method': 'REQUEST', 'name': 'src/static/ics/cal1.ics'})
    part.set_payload(open("src/static/ics/cal1.ics", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='src/static/ics/cal1.ics')

    msg.attach(part)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(send_from, password)

    session.sendmail(send_from, recipient, msg)
    session.quit()