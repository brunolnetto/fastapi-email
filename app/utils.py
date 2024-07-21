from jinja2 import Environment, FileSystemLoader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import smtplib
import time
import ssl
from uuid import uuid4

from .db import database
from .models import email_events
from .schemas import EmailSchema
from .config import settings, logger

env = Environment(loader=FileSystemLoader("app/templates"))

def render_template(template_filename: str, context: dict) -> str:
    template = env.get_template(template_filename)
    return template.render(context)

def get_timestamp_and_timezone() -> tuple:
    # Get the system timezone
    timezone = time.tzname[time.localtime().tm_isdst]

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return timestamp, timezone

async def register_email_event(
    subject: str, sender_email: str, recipient_email: str
):
    email_id = uuid4()
    query = email_events.insert().values(
        emev_id=email_id,
        emev_subject=subject,
        emev_sender_email=sender_email,
        emev_recipient_email=recipient_email,
        emev_status="pending",
        emev_created_at=datetime.now(),
        emev_sent_at=None,
        emev_opened_at=None
    )
    return email_id, await database.execute(query)

async def update_email_event_status(
    email_id: str, status: str, error_message: str = None
):
    query = email_events.update()\
        .where(email_events.c.emev_id == str(email_id))\
        .values(
            emev_status=status,
            emev_sent_at=datetime.now() if status == "sent" else None,    
            emev_error_message=error_message
        )
    await database.execute(query)

async def send_email_background(email: EmailSchema):
    email_id, _ = await register_email_event(
        email.subject, settings.SENDER_EMAIL, email.recipient_email
    )
    tracking_url=settings.tracking_url(email_id)
    timestamp, timezone = get_timestamp_and_timezone()

    context = {
        "recipient_name": email.recipient_name,
        "body": email.body,
        "sender_name": email.sender_name,
        "sender_email": settings.SENDER_EMAIL,
        "contact_url": settings.CONTANT_URL,
        "tracking_url": tracking_url,
        "subject": email.subject,
        "timestamp": timestamp,
        "timezone": timezone
    }

    html_content = render_template("html_template.html", context)

    # NOTE: The email is sent using the SMTP server
    sender_email = settings.SENDER_EMAIL

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = email.recipient_email
    message["Subject"] = email.subject
    
    part = MIMEText(html_content, "html")
    message.attach(part)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            settings.SMTP_SERVER, settings.SMTP_PORT, context=context
        ) as server:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(
                sender_email, email.recipient_email, message.as_string()
            )
        
        await update_email_event_status(email_id, "sent")
    except Exception as e:
        await update_email_event_status(email_id, "failed", str(e))
        logger.error(f"Failed to send email: {str(e)}")
