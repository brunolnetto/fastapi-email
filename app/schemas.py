from pydantic import BaseModel, EmailStr

class EmailSchema(BaseModel):
    recipient_email: EmailStr
    recipient_name: str
    subject: str
    body: str
    sender_name: str