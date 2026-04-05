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


class LeadScoreRequest(BaseModel):
    lead_id: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None


class LeadScoreResponse(BaseModel):
    lead_id: Optional[str] = None
    score: int
    intent: str
    summary: str
    recommended_action: str