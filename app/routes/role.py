from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models, auth
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.RoleResponse], summary="Get list of roles", description="Retrieve a list of roles with pagination.")
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Retrieve a list of roles with pagination.
    """
    return crud.get_roles(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.RoleResponse, summary="Create a new role", description="Create a new role with the provided details.")
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role with the provided details.
    """
    db_role = crud.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db, role)

@router.put("/{role_id}", response_model=schemas.RoleResponse, summary="Update role", description="Update role details.")
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Update role details.
    """
    db_role = crud.update_role(db, role_id, role_update)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.delete("/{role_id}", response_model=schemas.RoleResponse, summary="Delete role", description="Delete role by ID.")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_admin)):
    """
    Delete role by ID.
    """
    db_role = crud.delete_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role