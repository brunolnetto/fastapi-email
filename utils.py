from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import smtplib
import time
import ssl

from models import EmailSchema
from config import settings

env = Environment(loader=FileSystemLoader("templates"))

def render_template(template_filename: str, context: dict) -> str:
    template = env.get_template(template_filename)
    return template.render(context)

def send_email_background(email: EmailSchema):
    # Get the system timezone
    timezone = time.tzname[time.localtime().tm_isdst]

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    context = {
        "recipient_name": email.recipient_name,
        "body": email.body,
        "sender_name": email.sender_name,
        "sender_email": settings.SENDER_EMAIL,
        "contact_url": settings.CONTANT_URL,
        "subject": email.subject,
        "timestamp": timestamp,
        "timezone": timezone
    }

    html_content = render_template("html_template.html", context)

    message = MIMEMultipart("alternative")
    message["From"] = settings.SENDER_EMAIL
    message["To"] = email.recipient
    message["Subject"] = email.subject
    
    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            settings.SMTP_SERVER, 
            settings.SMTP_PORT, 
            context=context
        ) as server:
            server.login(
                settings.SMTP_USERNAME, settings.SMTP_PASSWORD
            )
            server.sendmail(
                settings.SENDER_EMAIL, email.recipient, message.as_string()
            )
    except Exception as e:
        # Handle or log the error if needed
        print(f"Failed to send email: {str(e)}")

