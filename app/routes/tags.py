from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role

router = APIRouter()

@router.get("/", response_model=list[schemas.TagResponse], summary="Get list of tags", description="Retrieve a list of tags with pagination.")
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Retrieve a list of tags with pagination.
    """
    return crud.get_tag(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.TagResponse, summary="Create new tag", description="Create new tag with the provided details.")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Create new tag with the provided details.
    """
    return crud.create_tag(db, tag)

@router.put("/{tag_id}", response_model=schemas.TagResponse, summary="Update tag", description="Update tag details.")
def update_tag(tag_id: int, tag_update: schemas.TagUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Update tag details.
    """
    db_tag = crud.update_tag(db, tag_id, tag_update)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/{tag_id}", response_model=schemas.TagResponse, summary="Delete tag", description="Delete tag by ID.")
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Delete tag by ID.
    """
    db_tag = crud.delete_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag