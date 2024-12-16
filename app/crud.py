from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name, email=user.email, hashed_password=hashed_password,
        is_active=user.is_active, is_admin=user.is_admin, role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user_update.name
        db_user.email = user_update.email
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        db_user.is_active = user_update.is_active
        db_user.is_admin = user_update.is_admin
        db_user.role = user_update.role
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_metadata_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MetaDataItem).offset(skip).limit(limit).all()

def create_metadata_item(db: Session, metadata_item: schemas.MetaDataItemCreate):
    db_metadata_item = models.MetaDataItem(**metadata_item.dict())
    db.add(db_metadata_item)
    db.commit()
    db.refresh(db_metadata_item)
    return db_metadata_item

def update_metadata_item(db: Session, metadata_item_id: int, metadata_item_update: schemas.MetaDataItemUpdate):
    db_metadata_item = db.query(models.MetaDataItem).filter(models.MetaDataItem.id == metadata_item_id).first()
    if db_metadata_item:
        db_metadata_item.key = metadata_item_update.key
        db_metadata_item.value = metadata_item_update.value
        db.commit()
        db.refresh(db_metadata_item)
    return db_metadata_item

def delete_metadata_item(db: Session, metadata_item_id: int):
    db_metadata_item = db.query(models.MetaDataItem).filter(models.MetaDataItem.id == metadata_item_id).first()
    if db_metadata_item:
        db.delete(db_metadata_item)
        db.commit()
    return db_metadata_item


def get_content(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Content).offset(skip).limit(limit).all()

def create_content(db: Session, content: schemas.ContentCreate):
    db_content = models.Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def update_content(db: Session, content_id: int, content_update: schemas.ContentUpdate):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if db_content:
        db_content.title = content_update.title
        db_content.body = content_update.body
        db.commit()
        db.refresh(db_content)
    return db_content

def delete_content(db: Session, content_id: int):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if db_content:
        db.delete(db_content)
        db.commit()
    return db_content

def get_category(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category_update.name
        db_category.description = category_update.description
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

def get_tag(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, tag_update: schemas.TagUpdate):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db_tag.name = tag_update.name
        db.commit()
        db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag
