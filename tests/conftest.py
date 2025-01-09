import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Ensure the app module can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Use a separate database for testing
SQLALCHEMY_DATABASE_URL = "postgresql://a_panel:backend@localhost/test_db"  # Replace with your actual test database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Drop the database tables
    Base.metadata.drop_all(bind=engine)