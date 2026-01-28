from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class UserRequest(BaseModel):
    email:EmailStr
    password:str=Field(min_length=6)

class UserResponse(BaseModel):
    email:EmailStr
    is_admin:bool
    created_at:str
    updated_at:str
class TokenResponse(BaseModel):
    token:str
    payload:dict
class TokenRequest(BaseModel):
    token:str