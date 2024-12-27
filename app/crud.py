from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
        role_id=user.role_id
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
        db_user.role_id = user_update.role_id
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_update: schemas.RoleUpdate):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role:
        db_role.name = role_update.name
        db_role.description = role_update.description
        db_role.permissions = role_update.permissions
        db_role.parent_id = role_update.parent_id
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def create_content(db: Session, content: schemas.ContentCreate):
    db_content = models.Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def get_content(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Content).offset(skip).limit(limit).all()

def update_content(db: Session, content_id: int, content_update: schemas.ContentUpdate):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if db_content:
        db_content.title = content_update.title
        db_content.body = content_update.body
        db_content.published = content_update.published
        db.commit()
        db.refresh(db_content)
    return db_content

def delete_content(db: Session, content_id: int):
    db_content = db.query(models.Content).filter(models.Content.id == content_id).first()
    if db_content:
        db.delete(db_content)
        db.commit()
    return db_content

def get_tags(db: Session, skip: int = 0, limit: int = 10):
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
        db_tag.description = tag_update.description
        db.commit()
        db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag

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
