from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Base user schema that will be inherited by other schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    role: str = "user"  # Add role field

# Schema for creating a new user, includes password
class UserCreate(UserBase):
    password: str

# Schema for updating an existing user, password is optional
class UserUpdate(UserBase):
    password: Optional[str] = None

# Schema for representing a user in responses (doesn't include password)
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries

# Schema for the token response when logging in
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for the token data (used for extracting info from the token payload)
class TokenData(BaseModel):
    email: Optional[str] = None  # Use Optional for nullable fields

class MetaDataItemBase(BaseModel):
    key: str
    value: str

class MetaDataItemCreate(MetaDataItemBase):
    pass

class MetaDataItemUpdate(MetaDataItemBase):
    pass

class MetaDataItemResponse(MetaDataItemBase):
    id: int

    class Config:
        orm_mode = True

class ContentBase(BaseModel):
    title: str
    body: str

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class ContentResponse(ContentBase):
    id: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    class Config:
        orm_mode = True
