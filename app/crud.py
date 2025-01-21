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
        db_user.role_id = user_update.role_id
        db_user.bio = user_update.bio  # Update bio
        db_user.profile_picture = user_update.profile_picture  # Update profile picture
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

def get_categories(db: Session, skip: int = 0, limit: int = 10):
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

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db_post.title = post_update.title
        db_post.body = post_update.body
        db_post.published = post_update.published
        db_post.category_id = post_update.category_id
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post

def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = comment_update.content
        db_comment.post_id = comment_update.post_id
        db_comment.user_id = comment_update.user_id
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

def search_posts(db: Session, query: str, skip: int = 0, limit: int = 10):
    return db.query(models.Post).filter(models.Post.title.ilike(f"%{query}%") | models.Post.body.ilike(f"%{query}%")).offset(skip).limit(limit).all()

def search_content(db: Session, query: str, skip: int = 0, limit: int = 10):
    return db.query(models.Content).filter(models.Content.title.ilike(f"%{query}%") | models.Content.body.ilike(f"%{query}%")).offset(skip).limit(limit).all()

def get_notifications(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: schemas.NotificationCreate):
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def update_notification(db: Session, notification_id: int, notification_update: schemas.NotificationUpdate):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification:
        db_notification.read = notification_update.read
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification
