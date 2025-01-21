import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[Dict[str, List[str]]] = {}  # Permissions as a dictionary
    parent_id: Optional[int] = None  # Parent role ID

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: Optional[dict] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    role_id: int
    bio: Optional[str] = None  # New field for user bio
    profile_picture: Optional[str] = None  # New field for profile picture URL

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    role_id: int
    role: RoleResponse
    bio: Optional[str] = None  # New field for user bio
    profile_picture: Optional[str] = None  # New field for profile picture URL

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
    published: Optional[bool] = None  

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

class PostBase(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None
    category_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int

    class Config:
        orm_mode = True

class NotificationBase(BaseModel):
    user_id: int
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    read: bool

class NotificationResponse(NotificationBase):
    id: int
    read: bool
    created_at: datetime

    class Config:
        orm_mode = True
