from pydantic import BaseModel, Field
from fastapi import Form


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)


class UserMultipartCreate(UserCreate):
    username: str = Form(..., min_length=3, max_length=50)
    password: str = Form(..., min_length=8)
