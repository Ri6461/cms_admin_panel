from pydantic import BaseModel, EmailStr
from typing import Optional, List

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    is_admin: bool = False
    role_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: RoleResponse

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

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
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    class Config:
        orm_mode = True
