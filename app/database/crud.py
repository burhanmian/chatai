from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import models, schemas


async def get_user_by_phone(db: AsyncSession, phone_number: str) -> Optional[models.User]:
    """Get user by phone number"""
    result = await db.execute(
        select(models.User).where(models.User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create new user"""
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update user"""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    db_user = result.scalar_one_or_none()
    if db_user:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def create_conversation(db: AsyncSession, conversation: schemas.ConversationCreate) -> models.Conversation:
    """Create new conversation"""
    db_conversation = models.Conversation(**conversation.model_dump())
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)
    return db_conversation


async def get_user_conversations(db: AsyncSession, user_id: int, limit: int = 10) -> List[models.Conversation]:
    """Get user conversations"""
    result = await db.execute(
        select(models.Conversation)
        .where(models.Conversation.user_id == user_id)
        .order_by(models.Conversation.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def create_payment(db: AsyncSession, payment: schemas.PaymentCreate) -> models.Payment:
    """Create new payment"""
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment


async def get_payment_by_reference(db: AsyncSession, reference_id: str) -> Optional[models.Payment]:
    """Get payment by reference ID"""
    result = await db.execute(
        select(models.Payment).where(models.Payment.reference_id == reference_id)
    )
    return result.scalar_one_or_none()


async def update_payment(db: AsyncSession, payment_id: int, payment_update: schemas.PaymentUpdate) -> Optional[models.Payment]:
    """Update payment"""
    result = await db.execute(
        select(models.Payment).where(models.Payment.id == payment_id)
    )
    db_payment = result.scalar_one_or_none()
    if db_payment:
        for key, value in payment_update.model_dump(exclude_unset=True).items():
            setattr(db_payment, key, value)
        await db.commit()
        await db.refresh(db_payment)
    return db_payment
