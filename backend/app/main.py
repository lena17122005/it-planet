from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models import User
from app.models.user import UserRole
from app.routers import admin, auth, companies, contacts, responses, users, vacancies

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(',') if origin.strip()],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        curator = db.query(User).filter(User.role == UserRole.curator).first()
        if not curator:
            db.add(
                User(
                    email="admin@tramplin.com",
                    display_name="Main Curator",
                    password_hash=hash_password("Admin12345!"),
                    role=UserRole.curator,
                    email_verified=True,
                )
            )
            db.commit()
    finally:
        db.close()


@app.get('/health')
def health() -> dict:
    return {'status': 'ok', 'service': settings.app_name}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(vacancies.router, prefix=settings.api_prefix)
app.include_router(companies.router, prefix=settings.api_prefix)
app.include_router(responses.router, prefix=settings.api_prefix)
app.include_router(contacts.router, prefix=settings.api_prefix)
app.include_router(admin.router, prefix=settings.api_prefix)
