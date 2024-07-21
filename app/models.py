from sqlalchemy import (
     Table, Column, Integer, String, DateTime, UUID,
)
from uuid import uuid4
from datetime import datetime

from .db import metadata

# Define table structure
email_events = Table(
    "email_events", metadata,
    Column("emev_id", UUID, primary_key=True, index=True, 
           unique=True, default=uuid4),
    Column("emev_subject", String),
    Column("emev_sender_email", String),
    Column("emev_recipient_email", String),
    Column("emev_status", String),  # e.g., 'pending', 'sent', 'failed'
    Column("emev_created_at", DateTime, default=datetime.now),
    Column("emev_sent_at", DateTime),
    Column("emev_opened_at", DateTime),
    Column("emev_error_message", String, nullable=True)
)
