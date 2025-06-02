from sqlalchemy import Column, Integer, String,UUID, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from api.db import Base
from datetime import datetime
from uuid import uuid4

class S4Model(Base):
    __tablename__ = "s4_storage"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    crc32 = Column(String(8), nullable=False, index=True, unique=True)
    file_name = Column(String(255), nullable=False, index=True)
    file_path = Column(String(255), nullable=False, index=True)
    compressed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    size = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    user = relationship("UserModel", back_populates="s4_storage")
