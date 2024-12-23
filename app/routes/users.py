from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models, auth
from app.database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse, summary="Register a new user", description="Register a new user with the provided details.")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with the provided details.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.UserResponse], summary="Get list of users", description="Retrieve a list of users with pagination.")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Retrieve a list of users with pagination.
    """
    return crud.get_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=schemas.UserResponse, summary="Update user", description="Update user details.")
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Update user details.
    """
    db_user = crud.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=schemas.UserResponse, summary="Delete user", description="Delete user by ID.")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Delete user by ID.
    """
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user