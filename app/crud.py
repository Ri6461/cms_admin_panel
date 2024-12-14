from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    """
    Fetch a user by their email address.

    Args:
        db (Session): Database session.
        email (str): Email of the user to retrieve.

    Returns:
        User: User object if found, None otherwise.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of users from the database with optional pagination.

    Args:
        db (Session): Database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[User]: List of users.
    """
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (schemas.UserCreate): User creation schema containing name, email, and password.

    Returns:
        User: The newly created user object.
    """
    hashed_password = get_password_hash(user.password)  # Hash the user's password.
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )
    db.add(db_user)  # Add the user to the session.
    db.commit()  # Commit the transaction.
    db.refresh(db_user)  # Refresh the session to include the new user's ID.
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """
    Update an existing user in the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to update.
        user_update (schemas.UserUpdate): User update schema containing updated name, email, and password.

    Returns:
        User: The updated user object.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user_update.name
        db_user.email = user_update.email
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        db_user.is_active = user_update.is_active
        db_user.is_admin = user_update.is_admin
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    Delete a user from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.

    Returns:
        User: The deleted user object.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
