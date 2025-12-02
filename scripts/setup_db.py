#!/usr/bin/env python3
"""
Database setup script
Creates all tables and optionally seeds with test data
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.session import init_db, AsyncSessionLocal
from app.database import models, schemas, crud


async def setup_database():
    """Initialize database and create tables"""
    print("Initializing database...")
    
    try:
        await init_db()
        print("✓ Database tables created successfully")
        
        # Optional: Create test user
        async with AsyncSessionLocal() as db:
            test_user = await crud.get_user_by_phone(db, "+923001234567")
            
            if not test_user:
                test_user = await crud.create_user(
                    db,
                    schemas.UserCreate(
                        phone_number="+923001234567",
                        name="Test User",
                        language_preference=models.LanguagePreference.ROMAN_URDU
                    )
                )
                print(f"✓ Test user created: {test_user.phone_number}")
            else:
                print(f"✓ Test user already exists: {test_user.phone_number}")
        
        print("\n✓ Database setup completed successfully!")
        
    except Exception as e:
        print(f"✗ Error setting up database: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(setup_database())
