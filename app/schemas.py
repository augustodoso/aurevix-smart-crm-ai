from pydantic import BaseModel, EmailStr
from typing import Optional


class ChatMessageIn(BaseModel):
    text: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None


class ChatMessageOut(BaseModel):
    intent: str
    reply: str
    salesforce_created: bool
    lead_id: Optional[str] = None