import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# SMTP Server details
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 465  # SSL
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', 'blueirisoft@zohomail.com')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')  # App-specific password from .env
FROM_EMAIL = SMTP_USERNAME
TO_EMAIL = "tahseen.blueiris@gmail.com"
SUBJECT = "Test Email from Zoho SMTP"
BODY = "Hello, this is a test email sent from Zoho SMTP using Python."

# Create MIME email object
msg = MIMEMultipart()
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = SUBJECT  # Fixed: Remove the dot, use the SUBJECT variable
msg.attach(MIMEText(BODY, "plain"))

# Connect to Zoho SMTP server
try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.set_debuglevel(1)  # Enable debugging output
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
