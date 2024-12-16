from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import router as api_router

# Create database tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="CMS Admin Panel",
    description="This is a backend for managing content and metadata.",
    version="1.0.0",
    contact={
        "name": "CMS Admin Panel Support",
        "url": "http://example.com/contact",
        "email": "support@example.com",
    },
    debug=True
)

# Include the API router
app.include_router(api_router, prefix="/api", tags=["API"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
