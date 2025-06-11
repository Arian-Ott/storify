from api.db import Base
from sqlalchemy import Column, String, Boolean, UUID, DateTime
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship


class UserModel(Base):
    """
    User model for the application.
    Those are the minimum fields required for the user to be created.
    Since storify does not require unnecessary data, email and other fields are considered optional and thus are handled in a different table to reduce overhead.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    email = Column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
        info={
            "description": "Optional email field for the user. Can be used for notifications or password recovery."
        },
    )
    email_verified = Column(
        Boolean,
        default=False,
        info={
            "description": "Indicates if the user's email is verified. This is separate from the user account being active."
        },
    )
    is_active = Column(
        Boolean,
        default=True,
        info={
            "description": "Indicates if the user account is active. Has nothing to do with the email verification of api/models/settings.py"
        },
    )
    created_at = Column(DateTime, default=datetime.now)
    last_password_change = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
