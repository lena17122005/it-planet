from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import admin, auth, companies, contacts, responses, users, vacancies

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(',') if origin.strip()],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


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
