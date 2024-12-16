from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app import crud, schemas, auth, models
from app.database import get_db

router = APIRouter()

@router.post("/token", response_model=schemas.Token, summary="Login for access token", description="Authenticate user and return an access token.")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
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

@router.post("/users/", response_model=schemas.UserResponse, summary="Create a new user", description="Create a new user with the provided details.")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.get("/users/", response_model=list[schemas.UserResponse], summary="Get list of users", description="Retrieve a list of users with pagination.")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    return crud.get_users(db, skip=skip, limit=limit)

@router.get("/users/me", response_model=schemas.UserResponse, summary="Get current user", description="Retrieve the details of the currently authenticated user.")
def read_users_me(current_user: schemas.UserResponse = Depends(auth.get_current_active_user)):
    return current_user

@router.put("/users/{user_id}", response_model=schemas.UserResponse, summary="Update a user", description="Update a user's details.")
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    db_user = crud.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=schemas.UserResponse, summary="Delete a user", description="Delete a user by ID.")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/metadata/", response_model=list[schemas.MetaDataItemResponse], summary="Get list of metadata items", description="Retrieve a list of metadata items with pagination.")
def read_metadata_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_metadata_items(db, skip=skip, limit=limit)

@router.post("/metadata/", response_model=schemas.MetaDataItemResponse, summary="Create a new metadata item", description="Create a new metadata item with the provided details.")
def create_metadata_item(metadata_item: schemas.MetaDataItemCreate, db: Session = Depends(get_db)):
    return crud.create_metadata_item(db, metadata_item)

@router.put("/metadata/{metadata_item_id}", response_model=schemas.MetaDataItemResponse, summary="Update a metadata item", description="Update a metadata item's details.")
def update_metadata_item(metadata_item_id: int, metadata_item_update: schemas.MetaDataItemUpdate, db: Session = Depends(get_db)):
    db_metadata_item = crud.update_metadata_item(db, metadata_item_id, metadata_item_update)
    if not db_metadata_item:
        raise HTTPException(status_code=404, detail="Metadata item not found")
    return db_metadata_item

@router.delete("/metadata/{metadata_item_id}", response_model=schemas.MetaDataItemResponse, summary="Delete a metadata item", description="Delete a metadata item by ID.")
def delete_metadata_item(metadata_item_id: int, db: Session = Depends(get_db)):
    db_metadata_item = crud.delete_metadata_item(db, metadata_item_id)
    if not db_metadata_item:
        raise HTTPException(status_code=404, detail="Metadata item not found")
    return db_metadata_item

@router.get("/content/", response_model=list[schemas.ContentResponse], summary="Get list of content", description="Retrieve a list of content with pagination.")
def read_content(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_content(db, skip=skip, limit=limit)

@router.post("/content/", response_model=schemas.ContentResponse, summary="Create new content", description="Create new content with the provided details.")
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db)):
    return crud.create_content(db, content)

@router.put("/content/{content_id}", response_model=schemas.ContentResponse, summary="Update content", description="Update content details.")
def update_content(content_id: int, content_update: schemas.ContentUpdate, db: Session = Depends(get_db)):
    db_content = crud.update_content(db, content_id, content_update)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.delete("/content/{content_id}", response_model=schemas.ContentResponse, summary="Delete content", description="Delete content by ID.")
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_content = crud.delete_content(db, content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.get("/categories/", response_model=list[schemas.CategoryResponse], summary="Get list of categories", description="Retrieve a list of categories with pagination.")
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_category(db, skip=skip, limit=limit)

@router.post("/categories/", response_model=schemas.CategoryResponse, summary="Create new category", description="Create new category with the provided details.")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@router.put("/categories/{category_id}", response_model=schemas.CategoryResponse, summary="Update category", description="Update category details.")
def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id, category_update)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/categories/{category_id}", response_model=schemas.CategoryResponse, summary="Delete category", description="Delete category by ID.")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.delete_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/tags/", response_model=list[schemas.TagResponse], summary="Get list of tags", description="Retrieve a list of tags with pagination.")
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_tag(db, skip=skip, limit=limit)

@router.post("/tags/", response_model=schemas.TagResponse, summary="Create new tag", description="Create new tag with the provided details.")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db, tag)

@router.put("/tags/{tag_id}", response_model=schemas.TagResponse, summary="Update tag", description="Update tag details.")
def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: Session = Depends(get_db)):
    db_tag = crud.update_tag(db, tag_id, tag_update)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/tags/{tag_id}", response_model=schemas.TagResponse, summary="Delete tag", description="Delete tag by ID.")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.delete_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
