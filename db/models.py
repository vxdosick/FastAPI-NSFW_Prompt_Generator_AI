from sqlalchemy import Column, String, Integer
from db.database import Base

class User(Base):
    __tablename__ = "users"

    telegram_id = Column(String, primary_key=True, index=True)
    credits = Column(Integer, default=0)