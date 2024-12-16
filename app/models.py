from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default="user")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role}, is_active={self.is_active}, is_admin={self.is_admin})>"

class MetaDataItem(Base):
    __tablename__ = "metadata_items"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    value = Column(String)
    content_id = Column(Integer, ForeignKey('content.id'))  # Add ForeignKey to link with Content
    content = relationship("Content", back_populates="metadata_items")  # Renamed from 'metadata'
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<MetaDataItem(id={self.id}, key={self.key}, value={self.value})>"

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Corrected table name
    tags = relationship("Tag", secondary="content_tags", back_populates="contents")
    metadata_items = relationship("MetaDataItem", back_populates="content")  # Renamed from 'metadata'
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Content(id={self.id}, title={self.title}, body={self.body}, category_id={self.category_id})>"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    contents = relationship("Content", secondary="content_tags", back_populates="tags")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"

class ContentTags(Base):
    __tablename__ = "content_tags"

    content_id = Column(Integer, ForeignKey('content.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)  # Corrected table name
