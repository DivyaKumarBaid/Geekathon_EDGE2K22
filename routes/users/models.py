from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# before validating user
class Pre_userdata(BaseModel):
    user: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    user_id: str = Field(...)
    email_token: str = Field(...)

# after validation of user
class User_data(BaseModel):
    user: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    user_id: str = Field(...)
    appointments :list[dict] = []
    approved_appointments :list[dict] = []

#user signup
class User(BaseModel):
    user: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
