import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch

from app.main import app
from app.db.session import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.users import User


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



@pytest.fixture(scope="module")
def client():

    Base.metadata.create_all(bind=engine)
    

    with TestClient(app) as c:
        yield c  
        

    Base.metadata.drop_all(bind=engine)



@pytest.fixture(scope="module")
def admin_headers(client): 
    db = TestingSessionLocal()
    
    
    admin_user = db.query(User).filter(User.phone == "1234567890").first()
    if not admin_user:
        admin_user = User(
            name="Admin",
            phone="1234567890",
            hashed_password=get_password_hash("testpass"),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    
    token = create_access_token(data={"sub": str(admin_user.id)})
    db.close()

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def service_id(client, admin_headers):
    response = client.post(
        "/service/create_service",
        json={
            "name": "Test_service",
            "duration_minutes": 60,
            "price": 100
        },
        headers=admin_headers
    )

    assert response.status_code == 200
    return response.json()["id"]


@pytest.fixture(scope="module")
def master_id(client, admin_headers, service_id):

    response = client.post(
        "/master/master_create",
        json={
            "name": "Test_Master",
            "phone": "1111111111",
            "specialization": "Barber"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    master_id = response.json()["id"]

    response = client.post(
        f"/master/{master_id}/add_service/{service_id}",
        headers=admin_headers
    )

    assert response.status_code == 200

    response = client.post(
        "/schedule/create_schedule",
        json={
            "master_id": master_id,
            "day_of_week": "Monday",
            "start_time": "09:00",
            "end_time": "18:00"
        },
        headers=admin_headers
    )

    assert response.status_code == 200

    return master_id


@pytest.fixture(scope="module")
def appointment(client, master_id, service_id):

    with patch(
        "app.api.appointments.cancel_unpaid_task.apply_async"
    ):

        payload = {
            "user_name": "Test_Client",
            "user_phone": "1231231231",
            "master_id": master_id,
            "service_id": service_id,
            "start_datetime": "2026-07-06T12:00"
        }

        response = client.post(
            "/appointments/appointment",
            json=payload
        )

        assert response.status_code == 200

        return response.json()