from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import crud, schemas, auth
from app.database import get_db

router = APIRouter()

# Login for access token
@router.post(
    "/token",
    response_model=schemas.Token,
    summary="Login for access token",
    description="Authenticate user and return an access token.",
)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Create a new user
@router.post(
    "/users/",
    response_model=schemas.UserResponse,
    summary="Create a new user",
    description="Create a new user with the provided details.",
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

# Get list of users
@router.get(
    "/users/",
    response_model=list[schemas.UserResponse],
    summary="Get list of users",
    description="Retrieve a list of users with pagination.",
)
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# Get current user
@router.get(
    "/users/me",
    response_model=schemas.UserResponse,
    summary="Get current user",
    description="Retrieve the details of the currently authenticated user.",
)
def read_users_me(
    current_user: schemas.UserResponse = Depends(auth.get_current_active_user),
):
    return current_user

# Update a user
@router.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    summary="Update a user",
    description="Update a user's details.",
)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete a user
@router.delete(
    "/users/{user_id}",
    response_model=schemas.UserResponse,
    summary="Delete a user",
    description="Delete a user by ID.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
