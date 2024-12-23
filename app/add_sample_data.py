if __name__ == "__main__":
    import sys
    import os
    import logging
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_sample_data():
    db: Session = SessionLocal()
    
    # Check if the sample category already exists
    sample_category = db.query(models.Category).filter_by(name="Sample Category").first()
    if not sample_category:
        # Add sample category if it does not exist
        sample_category = models.Category(
            name="Sample Category",
            description="This is a sample category."
        )
        db.add(sample_category)
        db.commit()
        db.refresh(sample_category)  # Refresh to get the generated ID
        logger.info(f"Added sample category: {sample_category.name}")

    # Add sample content
    sample_content = models.Content(
        title="Sample Content",
        body="This is a sample content.",
        category_id=sample_category.id  # Use the generated ID of the sample category
    )
    db.add(sample_content)
    db.commit()
    db.refresh(sample_content)  # Refresh to get the generated ID
    logger.info(f"Added sample content: {sample_content.title}")

    # Add sample metadata items
    sample_metadata_items = [
        models.MetaDataItem(key="author", value="John Doe", content_id=sample_content.id),
        models.MetaDataItem(key="keywords", value="fastapi, sqlalchemy", content_id=sample_content.id),
    ]
    for item in sample_metadata_items:
        db.add(item)
    
    db.commit()
    logger.info(f"Added sample metadata items for content ID: {sample_content.id}")
    db.close()

if __name__ == "__main__":
    add_sample_data()