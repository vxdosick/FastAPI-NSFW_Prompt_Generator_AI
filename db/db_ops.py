from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User

# Variables
START_CREDITS = 5

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(telegram_id: str, db: Session):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(telegram_id: str, credits: int, db: Session):
    user = User(telegram_id=telegram_id, credits=credits)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_or_create_user(user_id: str, db):
    user = get_user(user_id, db)
    if not user:
        user = create_user(user_id, START_CREDITS, db)
    return user

def add_credits(telegram_id: str, credits: int, db: Session):
    user = get_user(telegram_id, db)
    user.credits += credits
    db.commit()
    db.refresh(user)