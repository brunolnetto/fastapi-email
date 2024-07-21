from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from datetime import datetime

from .exceptions import SendEmailException
from .utils import send_email_background, get_timestamp_and_timezone
from .schemas import EmailSchema
from .db import init_db, close_db, database
from .models import email_events
from .config import settings, logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()  

app = FastAPI(
    title="Email Service",
    description="This is a simple email service",
    version="0.0.1",
    docs_url="/",
    lifespan=lifespan
)


@app.get("/track/{email_id}")
async def track_email(email_id: str):
    # Update email event with the timestamp of when the email was opened
    query = email_events.update()\
        .where(email_events.c.emev_id == email_id)\
        .values(emev_opened_at=datetime.now(), emev_status="opened")
    
    await database.execute(query)
    # Return a 1x1 pixel transparent GIF
    transparent_pixel='R0lGODlhAQABAIAAAAAAACH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
    transparent_pixel_html = (
        f'<html><body><img src="data:image/gif;base64,{transparent_pixel}"></body></html>'
    )
    return HTMLResponse(content=transparent_pixel_html, media_type="text/html")


@app.post("/send-email/")
async def send_email(
    email: EmailSchema, background_tasks: BackgroundTasks
):
    """
    This endpoint is used to send an email in the background

    >> curl -X POST "http://localhost:8000/send-email/" \
        -H "Content-Type: application/json" \
        -d '{
            "recipient_name": "John Doe",
            "recipient": f"{settings.SENDER_EMAIL}",
            "sender_name": "Jane Doe",
            "subject": "Test Email",
            "body": "This is a test email"
        }'
    """

    background_tasks.add_task(send_email_background, email)
    
    return {"message": "Email is being sent in the background"}

@app.post("/test-email/")
async def test_email(background_tasks: BackgroundTasks):
    """
    This endpoint is used to test the email sending functionality

    >> curl -X POST "http://localhost:8000/test-email/"
    """

    email = EmailSchema(
        recipient_name="Myself",
        recipient_email=settings.SENDER_EMAIL,
        sender_name="Email service",
        subject="Test Email",
        body="This is a test email"
    )
    
    try:
        background_tasks.add_task(send_email_background, email)
    except Exception as e:
        raise SendEmailException(e)
    
    return {"message": "Email sent in background"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
