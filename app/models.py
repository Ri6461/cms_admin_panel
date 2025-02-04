from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    """
    Role model representing a user role in the system.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    permissions = Column(JSON)
    parent_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    parent = relationship("Role", remote_side=[id], backref="children")
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}, description={self.description})>"

class User(Base):
    """
    User model representing a user in the system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    bio = Column(Text, nullable=True)  # New field for user bio
    profile_picture = Column(String, nullable=True)  # New field for profile picture URL

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="users")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    comments = relationship("Comment", order_by="Comment.id", back_populates="user")
    notifications = relationship("Notification", order_by="Notification.id", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role.name}, is_active={self.is_active})>"

class MetaDataItem(Base):
    """
    MetaDataItem model representing metadata associated with content.
    """
    __tablename__ = "metadata_items"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    value = Column(String)
    content_id = Column(Integer, ForeignKey('content.id'))
    content = relationship("Content", back_populates="metadata_items")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<MetaDataItem(id={self.id}, key={self.key}, value={self.value})>"

class Content(Base):
    """
    Content model representing the main content in the system.
    """
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    published = Column(Boolean, default=False)  
    category_id = Column(Integer, ForeignKey('categories.id'))  # Corrected table name
    tags = relationship("Tag", secondary="content_tags", back_populates="contents")
    metadata_items = relationship("MetaDataItem", back_populates="content")  # Renamed from 'metadata'
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Content(id={self.id}, title={self.title}, body={self.body}, category_id={self.category_id}, published={self.published})>"

class Category(Base):
    """
    Category model representing categories for content.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"

class Tag(Base):
    """
    Tag model representing tags associated with content.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True) 
    contents = relationship("Content", secondary="content_tags", back_populates="tags")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

class ContentTags(Base):
    """
    Association table for many-to-many relationship between Content and Tag.
    """
    __tablename__ = "content_tags"

    content_id = Column(Integer, ForeignKey('content.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class Post(Base):
    """
    Post model representing blog posts or articles.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    published = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="posts")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    comments = relationship("Comment", order_by="Comment.id", back_populates="post")

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title}, body={self.body}, category_id={self.category_id}, published={self.published})>"

Category.posts = relationship("Post", order_by=Post.id, back_populates="category")

class Comment(Base):
    """
    Comment model representing comments on posts.
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, content={self.content}, post_id={self.post_id}, user_id={self.user_id})>"

Post.comments = relationship("Comment", order_by=Comment.id, back_populates="post")
User.comments = relationship("Comment", order_by=Comment.id, back_populates="user")

class Notification(Base):
    """
    Notification model representing notifications for users.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="notifications")

User.notifications = relationship("Notification", order_by=Notification.id, back_populates="user")
