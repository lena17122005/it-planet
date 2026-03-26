import os
from pathlib import Path

from fastapi.testclient import TestClient

# Isolated sqlite DB for E2E tests.
os.environ['DATABASE_URL'] = f"sqlite:///{Path(__file__).parent / 'test.db'}"

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.core.security import hash_password  # noqa: E402


client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.add(User(email='admin@tramplin.com', display_name='Main Curator', password_hash=hash_password('Admin12345!'), role=UserRole.curator, email_verified=True))
        db.commit()
    finally:
        db.close()


def _register_user(email: str, role: str):
    payload = {
        'email': email,
        'display_name': role,
        'password': 'Password123',
        'role': role,
    }
    if role == 'employer':
        payload.update({'company_name': 'Acme', 'inn': '1234567890', 'corporate_email': 'hr@acme.ru'})
    response = client.post('/api/v1/auth/register', json=payload)
    assert response.status_code == 200
    return response.json()


def test_full_happy_path_auth_refresh_and_vacancy_flow():
    # seeker + employer + curator accounts
    seeker_tokens = _register_user('seeker@example.com', 'seeker')
    employer_tokens = _register_user('employer@example.com', 'employer')

    # Email verification
    verify = client.post('/api/v1/auth/verify-email', json={'email': 'seeker@example.com', 'code': '123456'})
    assert verify.status_code == 200

    # Refresh flow
    refreshed = client.post('/api/v1/auth/refresh', json={'refresh_token': seeker_tokens['refresh_token']})
    assert refreshed.status_code == 200
    assert 'access_token' in refreshed.json()

    # Employer creates vacancy
    vacancy_payload = {
        'title': 'Python Intern',
        'description': 'Build APIs and tests',
        'type': 'internship',
        'format': 'hybrid',
        'city': 'Москва',
        'address': 'Москва, Кремль',
        'tags': ['Python', 'FastAPI'],
    }
    create_vacancy = client.post(
        '/api/v1/vacancies',
        json=vacancy_payload,
        headers={'Authorization': f"Bearer {employer_tokens['access_token']}"},
    )
    assert create_vacancy.status_code == 200
    vacancy_id = create_vacancy.json()['id']

    # Curator publishes vacancy from pending queue
    curator_login = client.post('/api/v1/auth/login', json={'email': 'admin@tramplin.com', 'password': 'Admin12345!'})
    assert curator_login.status_code == 200
    curator_token = curator_login.json()['access_token']

    publish = client.patch(f'/api/v1/admin/vacancies/{vacancy_id}/publish', headers={'Authorization': f'Bearer {curator_token}'})
    assert publish.status_code == 200

    # Seeker responds to vacancy
    respond = client.post(
        '/api/v1/responses',
        json={'vacancy_id': vacancy_id, 'note': 'Готов пройти тестовое'},
        headers={'Authorization': f"Bearer {seeker_tokens['access_token']}"},
    )
    assert respond.status_code == 200

    # Seeker sends contact request (self-check negative scenario)
    db = SessionLocal()
    try:
        seeker_id = db.query(User).filter(User.email == 'seeker@example.com').first().id
    finally:
        db.close()
    bad_request = client.post('/api/v1/contacts/request', json={'receiver_id': seeker_id}, headers={'Authorization': f"Bearer {seeker_tokens['access_token']}"})
    assert bad_request.status_code in (400, 404)
