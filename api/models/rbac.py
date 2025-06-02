from api.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
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

    users = relationship("UserModel", back_populates="role")


class UserRoleModel(Base):
    """
    User-Role association model for the application.
    """

    __tablename__ = "user_roles"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("UserModel", back_populates="roles")
    role = relationship("RoleModel", back_populates="users")
