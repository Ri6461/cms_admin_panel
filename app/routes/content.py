from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role, check_permissions

router = APIRouter()

@router.get("/", response_model=list[schemas.ContentResponse], summary="Get list of content", description="Retrieve a list of content with pagination.")
def read_content(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "content", "read")
    return crud.get_content(db, skip=skip, limit=limit)

@router.get("/search", response_model=list[schemas.ContentResponse], summary="Search content", description="Search content by title or body.")
def search_content(query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "content", "read")
    return crud.search_content(db, query, skip=skip, limit=limit)

@router.post("/", response_model=schemas.ContentResponse, summary="Create new content", description="Create new content with the provided details.")
def create_content(content: schemas.ContentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "content", "create")
    return crud.create_content(db, content)

@router.put("/{content_id}", response_model=schemas.ContentResponse, summary="Update content", description="Update content details.")
def update_content(content_id: int, content_update: schemas.ContentUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "content", "update")
    db_content = crud.update_content(db, content_id, content_update)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@router.delete("/{content_id}", response_model=schemas.ContentResponse, summary="Delete content", description="Delete content by ID.")
def delete_content(content_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "content", "delete")
    db_content = crud.delete_content(db, content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content