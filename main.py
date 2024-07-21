from fastapi import FastAPI, BackgroundTasks, HTTPException
from utils import send_email_background
from models import EmailSchema

app = FastAPI()

@app.post("/send-email/")
async def send_email(
    email: EmailSchema, background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email_background, email)
    return {"message": "Email is being sent in the background"}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
