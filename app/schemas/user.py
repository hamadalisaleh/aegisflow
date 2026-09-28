from pydantic import BaseModel, EmailStr
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> 9c4d87fab85b1e106f349f81a2e7ae6eee30e18b

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    role: str
    is_active: bool
<<<<<<< HEAD
    created_at: datetime | None = None
=======
>>>>>>> 9c4d87fab85b1e106f349f81a2e7ae6eee30e18b

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str