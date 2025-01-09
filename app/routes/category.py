from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role, check_permissions

router = APIRouter()

@router.get("/", response_model=list[schemas.CategoryResponse], summary="Get list of categories", description="Retrieve a list of categories with pagination.")
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "categories", "read")
    return crud.get_categories(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.CategoryResponse, summary="Create a new category", description="Create a new category with the provided details.")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "categories", "create")
    return crud.create_category(db, category)

@router.put("/{category_id}", response_model=schemas.CategoryResponse, summary="Update category", description="Update category details.")
def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "categories", "update")
    db_category = crud.update_category(db, category_id, category_update)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", response_model=schemas.CategoryResponse, summary="Delete category", description="Delete category by ID.")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "categories", "delete")
    db_category = crud.delete_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category