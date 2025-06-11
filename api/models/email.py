from api.db import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


class EmailToken(Base):
    """
    Model to store email verification tokens.
    This is used to verify the email address of the user.
    """

    __tablename__ = "email_tokens"

    token = Column(String(32), nullable=False, primary_key=True)

    profile_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    issued_because = Column(
        String(32),
        nullable=False,
        info={
            "description": "Reason for issuing the token, e.g., 'email_verification', 'password_reset', etc."
        },
    )
