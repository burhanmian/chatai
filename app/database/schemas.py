from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.database.models import LanguagePreference, MessageType, PaymentStatus, PaymentProvider


class UserBase(BaseModel):
    phone_number: str
    name: Optional[str] = None
    language_preference: LanguagePreference = LanguagePreference.ENGLISH


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    language_preference: Optional[LanguagePreference] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    message_type: MessageType
    user_message: str
    ai_response: str
    audio_transcript: Optional[str] = None


class ConversationCreate(ConversationBase):
    user_id: int


class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    provider: PaymentProvider
    amount: float
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    user_id: int
    reference_id: str


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None


class Payment(PaymentBase):
    id: int
    user_id: int
    status: PaymentStatus
    reference_id: str
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
