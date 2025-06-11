from api.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from datetime import datetime


class RoleModel(Base):
    """
    Role model for the application.
    """

    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False, index=True, primary_key=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
