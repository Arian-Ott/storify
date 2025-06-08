from sqlalchemy import Column, String, UUID, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from api.db import Base
from datetime import datetime


class S4Model(Base):
    __tablename__ = "s4_storage"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    file_hash = Column(String(128), nullable=False, unique=True, index=True)
    compressed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class S4Symlink(Base):
    __tablename__ = "s4_symlink"
    id = Column(UUID(as_uuid=True), primary_key=True)

    source_id = Column(
        UUID(as_uuid=True),
        ForeignKey("s4_storage.id", ondelete="CASCADE"),
        nullable=False,
    )
    file_name = Column(String(255), nullable=False, unique=False, index=True)

    source = relationship("S4Model", foreign_keys=[source_id])
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
