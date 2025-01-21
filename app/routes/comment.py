from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role, check_permissions

router = APIRouter()

@router.get("/", response_model=list[schemas.CommentResponse], summary="Get list of comments", description="Retrieve a list of comments with pagination.")
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "comments", "read")
    return crud.get_comments(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.CommentResponse, summary="Create a new comment", description="Create a new comment with the provided details.")
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "comments", "create")
    return crud.create_comment(db, comment)

@router.put("/{comment_id}", response_model=schemas.CommentResponse, summary="Update comment", description="Update comment details.")
def update_comment(comment_id: int, comment_update: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "comments", "update")
    db_comment = crud.update_comment(db, comment_id, comment_update)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.delete("/{comment_id}", response_model=schemas.CommentResponse, summary="Delete comment", description="Delete comment by ID.")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "comments", "delete")
    db_comment = crud.delete_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment