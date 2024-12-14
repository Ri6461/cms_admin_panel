from fastapi import FastAPI, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.openapi.models import SecurityScheme as SecuritySchemeModel
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app import models
from app.database import engine
from app.routes import router as user_router

# Create database tables if they don't exist already
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Admin Panel",
    description="This is an admin panel for managing users and authentication.",
    version="1.0.0",
    contact={
        "name": "Admin Panel Support",
        "url": "http://example.com/contact",
        "email": "support@example.com",
    },
    debug=True
)

# Define OAuth2PasswordBearer instance for token generation and usage
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# Mount static files for serving assets (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates/")

# Include the user routes, with the prefix `/api` and the tag "Users"
app.include_router(user_router, prefix="/api", tags=["Users"])

# Example route: Home/dashboard page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Render the admin panel dashboard.
    """
    return templates.TemplateResponse("template.html", {"request": request, "page": "home"})

# Example route: Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """
    Render the login page.
    """
    return templates.TemplateResponse("template.html", {"request": request, "page": "login"})

# Example route: User management page
@app.get("/users", response_class=HTMLResponse)
def users_page(request: Request):
    """
    Render the user management page.
    """
    return templates.TemplateResponse("template.html", {"request": request, "page": "users"})
