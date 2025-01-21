from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role, check_permissions

router = APIRouter()

@router.get("/", response_model=list[schemas.PostResponse], summary="Get list of posts", description="Retrieve a list of posts with pagination.")
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "posts", "read")
    return crud.get_posts(db, skip=skip, limit=limit)

@router.get("/search", response_model=list[schemas.PostResponse], summary="Search posts", description="Search posts by title or body.")
def search_posts(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "posts", "read")
    return crud.search_posts(db, query, skip=skip, limit=limit)

@router.post("/", response_model=schemas.PostResponse, summary="Create a new post", description="Create a new post with the provided details.")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "posts", "create")
    return crud.create_post(db, post)

@router.put("/{post_id}", response_model=schemas.PostResponse, summary="Update post", description="Update post details.")
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "posts", "update")
    db_post = crud.update_post(db, post_id, post_update)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.delete("/{post_id}", response_model=schemas.PostResponse, summary="Delete post", description="Delete post by ID.")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "posts", "delete")
    db_post = crud.delete_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post