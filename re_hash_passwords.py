from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.utils import get_password_hash  # Updated import

def re_hash_passwords():
    db: Session = SessionLocal()
    users = db.query(models.User).all()
    for user in users:
        # Re-hash the password using argon2
        new_hashed_password = get_password_hash(user.hashed_password)
        user.hashed_password = new_hashed_password
        db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    re_hash_passwords()