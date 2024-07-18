import csv
import smtplib
import imaplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import datetime
import pytz


tz_karachi=pytz.timezone('Asia/Karachi')
# CSV file containing id, email, and name
csv_file_path = '/content/emails_adicto_users.csv'

# SMTP (sending) server details
smtp_server = 'smtp.titan.email'
smtp_port = 587

# IMAP (receiving) server details
imap_server = 'imap.titan.email'
imap_port = 993

# Sender's email and password
sender_email = ''
sender_password = ''


def send_email(recipient_email, recipient_name, recipient_id):
    # Create the message
    message = MIMEMultipart("alternative") 
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = Header('Bonus Credits from Adicto', 'utf-8')

    # Greet the recipient by name in the email body
    #body = f'Hi {recipient_name},\n'
    html=f"""
          <html>
          <body>
          	<p>Hi {recipient_name},</p>
            <p>We trust this message finds you well and in high spirits. We appreciate your patience and understanding as we've been working to enhance your experience with the Adicto app.</p>
            <p><b>Exciting news!</b> The upgraded version of the Adicto app is now live and ready for you to explore! 🚀 Head to the  <a href="https://adictoai.us9.list-manage.com/track/click?u=4a3680972972c66068954063c&id=c135cc4593&e=a56b89ccd9">Google Play Store</a> to download the latest version and enjoy an even smoother and more enriched creative journey.<p>
            <p>As a token of our gratitude for your ongoing support, <b>Adicto is thrilled to reward you with bonus credits</b>. Your role in the Addicto community is invaluable to us, and ensuring your satisfaction is our top priority.</p>
            <p>Thank you for your continued support and dedication to Adicto. Feel free to dive into the upgraded features and functionalities and let your creativity soar with Addicto.</p>
            <p>If you have any further questions or would like to share your feedback, our support team at <a href="mailto:contact@adictoai.com">contact@adictoai.com</a> is here to assist you and ensure your Addicto experience is nothing short of amazing.</p>
            <p>We look forward to witnessing your incredible creations on Adicto!</p>
            <p>Best Regards,<br>Team Adicto</p>
            <a href="https://adictoai.us9.list-manage.com/track/click?u=4a3680972972c66068954063c&id=c135cc4593&e=a56b89ccd9"><center> <img src="https://lh3.googleusercontent.com/pw/ABLVV86hzSga84fPbnjRa_txot05mqMiJdpu8m86Lmx0atzyqzwTYPieGZkWMv48wcLEQ6hbSlDNZyU90ITabyPxMbBVwCcAO41xufuicVMv1rIEnYz2x1ohfQtIJjYT0uzpwRk_A4u169HflbuKzuc4M4Sn=w700-h350-s-no?authuser=0"></center></a>
          </body>
        </html>

    """


    #text_part = MIMEText(body, 'plain', 'utf-8')
    html_part=MIMEText(html,'html')
    #message.attach(text_part)
    message.attach(html_part)

    # Attach the file (modify as needed)
#   attachment_path = '/content/unnamed.jpg'
#    with open(attachment_path, 'rb') as attachment:
#        part = MIMEBase('application', 'octet-stream')
#        part.set_payload(attachment.read())
#        encoders.encode_base64(part)
#        part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
#        message.attach(part)

    try:
        # Send the email
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        smtp_obj.starttls()
        smtp_obj.login(sender_email, sender_password)
        smtp_obj.sendmail(sender_email, recipient_email, message.as_string())
        smtp_obj.quit()
        #print(f'Email sent successfully to {recipient_name} ({recipient_email}).')

        # Append the sent email to the IMAP server's "Sent" folder
        imap_obj = imaplib.IMAP4_SSL(imap_server, imap_port)
        imap_obj.login(sender_email, sender_password)
        imap_obj.append('Sent', '', imaplib.Time2Internaldate(imaplib.Time2Internaldate(imaplib.Time2Internaldate(time.time()))), message.as_bytes())
        imap_obj.logout()

        print(f'Last sent email details - ID: {recipient_id}, Name: {recipient_name}, Email: {recipient_email}')
        print(datetime.datetime.now(tz_karachi))
    except smtplib.SMTPException as e:
        print(f'Error sending email  to {recipient_name} ({recipient_email}): {str(e)}')
    except imaplib.IMAP4.error as e:
        print(f'Error appending email to {recipient_name} ({recipient_email}) to "Sent" folder: {str(e)}')
import csv
import time

start = 848
stop = 1148
batch_size = 49
total_batches = 5
row_counter = 0
batch_counter = 0

with open(csv_file_path, 'r') as csv_file:

    while batch_counter < total_batches:
        csv_reader = csv.DictReader(csv_file)  
        for row in csv_reader:
            row_counter += 1

            if start <= row_counter <= stop:
                recipient_email = row['email']
                recipient_name = row['name']
                recipient_id = row['id']

                send_email(recipient_email, recipient_name, recipient_id)

                if row_counter == start + batch_size:
                    batch_counter += 1
                    if batch_counter < total_batches:
                        print(f"Pausing for 1 hour before the next batch (Batch {batch_counter + 1}/{total_batches})")
                        time.sleep(3600)
                    break

            elif row_counter > stop:
                break
