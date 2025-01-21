from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_active_user_with_role, check_permissions

router = APIRouter()

@router.get("/", response_model=list[schemas.NotificationResponse], summary="Get list of notifications", description="Retrieve a list of notifications with pagination.")
def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "notifications", "read")
    return crud.get_notifications(db, current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.NotificationResponse, summary="Create a new notification", description="Create a new notification with the provided details.")
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "notifications", "create")
    return crud.create_notification(db, notification)

@router.put("/{notification_id}", response_model=schemas.NotificationResponse, summary="Update notification", description="Update notification details.")
def update_notification(notification_id: int, notification_update: schemas.NotificationUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "notifications", "update")
    db_notification = crud.update_notification(db, notification_id, notification_update)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification

@router.delete("/{notification_id}", response_model=schemas.NotificationResponse, summary="Delete notification", description="Delete notification by ID.")
def delete_notification(notification_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user_with_role("Admin", "Super Admin"))):
    check_permissions(current_user, "notifications", "delete")
    db_notification = crud.delete_notification(db, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return db_notification