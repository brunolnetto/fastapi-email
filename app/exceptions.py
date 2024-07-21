from fastapi import HTTPException

class SendEmailException(Exception):
    def __init__(self, e: Exception):
        self.status_code = 500
        self.message = f"Failed to send email: {str(e)}"