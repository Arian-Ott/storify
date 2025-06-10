from api.db import Base
from sqlalchemy import Column, String, UUID, DateTime, ForeignKey, Integer
from api.models.user import UserModel
from datetime import datetime, timedelta


class EmailTokenModel(Base):
    """
    Model for storing email tokens.
    """

    __tablename__ = "email_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(UUID(), nullable=False, unique=True, index=True)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = Column(UserModel, back_populates="email_tokens")
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, default=datetime.now + timedelta(minutes=30))

class EmailTokenReason(Base):
    __tablename__ = "email_token_cause"
    cause = Column(String(50), primary_key=True, nullable=False)
    
    

    