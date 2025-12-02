from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.database import crud, schemas

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[schemas.User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all users"""
    # In production, add authentication
    return []


@router.get("/users/{phone_number}", response_model=schemas.User)
async def get_user(
    phone_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Get user by phone number"""
    user = await crud.get_user_by_phone(db, phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Get user conversations"""
    conversations = await crud.get_user_conversations(db, user_id, limit)
    return conversations


@router.get("/payments/{reference_id}")
async def get_payment(
    reference_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get payment by reference ID"""
    payment = await crud.get_payment_by_reference(db, reference_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
