from api.db import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime, UUID, ForeignKey
from datetime import datetime
import uuid


class UserProfile(Base):
    """Optional user profile settings for the application. Since storify does not require unnecessary data, email and other fields are considered optional. In normal applications, these fields are expected to be part of the user entry itself. However, having fields in the table filled with null by default creates unnecessary overhead in the database. Therefore, these fields are optional and can be added later if needed."""

    __tablename__ = "user_profiles"

    id = Column(ForeignKey("users.id"), primary_key=True, nullable=False)
    email = Column(String(255), nullable=True, unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
