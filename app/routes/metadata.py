from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role

router = APIRouter()

@router.get("/", response_model=list[schemas.MetaDataItemResponse], summary="Get list of metadata items", description="Retrieve a list of metadata items with pagination.")
def read_metadata_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Retrieve a list of metadata items with pagination.
    """
    return crud.get_metadata_items(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.MetaDataItemResponse, summary="Create a new metadata item", description="Create a new metadata item with the provided details.")
def create_metadata_item(metadata_item: schemas.MetaDataItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Create a new metadata item with the provided details.
    """
    return crud.create_metadata_item(db, metadata_item)

@router.put("/{metadata_item_id}", response_model=schemas.MetaDataItemResponse, summary="Update a metadata item", description="Update a metadata item's details.")
def update_metadata_item(metadata_item_id: int, metadata_item_update: schemas.MetaDataItemUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Update a metadata item's details.
    """
    db_metadata_item = crud.update_metadata_item(db, metadata_item_id, metadata_item_update)
    if not db_metadata_item:
        raise HTTPException(status_code=404, detail="Metadata item not found")
    return db_metadata_item

@router.delete("/{metadata_item_id}", response_model=schemas.MetaDataItemResponse, summary="Delete a metadata item", description="Delete a metadata item by ID.")
def delete_metadata_item(metadata_item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin"))):
    """
    Delete a metadata item by ID.
    """
    db_metadata_item = crud.delete_metadata_item(db, metadata_item_id)
    if not db_metadata_item:
        raise HTTPException(status_code=404, detail="Metadata item not found")
    return db_metadata_item