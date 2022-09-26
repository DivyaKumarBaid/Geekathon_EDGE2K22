import smtplib
from email.message import EmailMessage
import config.database as database
import os
from dotenv import load_dotenv

load_dotenv()


def appointment_email(doc_id: str, user_id: str, app_date: str, app_time: str, online: bool):

    cursor2 = database.docs.find_one({"doc_id": doc_id})
    cursor3 = database.user_col.find_one({"user_id": user_id})
    if online:
        mode = " Online/Virtual "
    else:
        mode = "Offline"
    mailsTosend = [cursor2["email"], cursor3["email"]]

    for i in mailsTosend:
        message = EmailMessage()
        # The mail addresses and password
        recievers_mail = i
        sender_address = os.getenv('EMAILADD')
        sender_pass = os.getenv('EMAILPASS')
        message['From'] = sender_address
        message['To'] = recievers_mail
        # The subject line
        message['Subject'] = 'Appointment Notification'

        # Setup the MIME

        message.set_content(
            f'''
      <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Appointment have been scheduled.</title>
          <style>
            .wrapper {{
              padding: 20px;
              color: #444;
              font-size: 1.3em;
            }}
            a {{
              background: #592f80;
              text-decoration: none;
              padding: 8px 15px;
              border-radius: 5px;
              color: #fff;
            }}
          </style>
        </head>
        <body>
          <div class="wrapper">
            <p>Thank You for using Well_being.</p>
            <p>An appointment have been marked by {cursor3['user']} for {cursor2['doc']} on {app_date} starting at {app_time}</p>
            <p>The appointment is in {mode}.</p>
            <br>
          </div>
        </body>
        </html>
          ''',
            subtype="html")

        # The body and the attachments for the mail
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        # login with mail_id and password
        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, recievers_mail, text)
        print('Mail Sent')
        session.quit()
