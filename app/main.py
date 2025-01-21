from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routes import content, metadata, tags, users, role, auth_routes, category, post, comment

# Create database tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="CMS Admin Panel",
    description="This is a CMS admin panel for managing content, metadata, users, roles, and tags.",
    version="1.0.0",
    contact={
        "name": "CMS Admin Panel Support",
        "url": "http://example.com/contact",
        "email": "support@example.com",
    },
    debug=True
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(content.router, prefix="/api/content", tags=["Content"])
app.include_router(metadata.router, prefix="/api/metadata", tags=["Metadata"])
app.include_router(tags.router, prefix="/api/tags", tags=["Tags"])
app.include_router(role.router, prefix="/api/roles", tags=["Roles"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(category.router, prefix="/api/categories", tags=["Categories"])
app.include_router(post.router, prefix="/api/posts", tags=["Posts"])
app.include_router(comment.router, prefix="/api/comments", tags=["Comments"])

@app.get("/", summary="Root Endpoint", description="Welcome to the CMS Admin Panel API.")
def read_root():
    """
    Root endpoint that provides a welcome message.
    """
    return {"message": "Welcome to the CMS Admin Panel API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
