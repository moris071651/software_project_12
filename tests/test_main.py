from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base
from app.utils.dep import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_patient_data(test_doctor_data):
    doc_response = client.post("/api/v1/auth/register/doctor", json=test_doctor_data)
    doctor_id = doc_response.json()["id"]
    
    return {
        "name": "John Doe",
        "phone": "0888888888",
        "email": "john@example.com",
        "password": "securepassword123",
        "doctor_id": doctor_id
    }

@pytest.fixture
def test_doctor_data():
    return {
        "name": "Dr. Smith",
        "address": "here_and_there",
        "email": "smith@hospital.com",
        "password": "docpassword123"
    }

@pytest.fixture
def patient_token(test_patient_data):
    client.post("/api/v1/auth/register/patient", json=test_patient_data)
    login_data = {"email": test_patient_data["email"], "password": test_patient_data["password"]}
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json()}")
    return response.json()["token"]

@pytest.fixture
def doctor_token(test_doctor_data):
    login_data = {"email": test_doctor_data["email"], "password": test_doctor_data["password"]}
    response = client.post("/api/v1/auth/login", json=login_data)
    
    if response.status_code != 200:
        client.post("/api/v1/auth/register/doctor", json=test_doctor_data)
        response = client.post("/api/v1/auth/login", json=login_data)
        
    return response.json()["token"]

def test_register_patient(test_patient_data):
    response = client.post("/api/v1/auth/register/patient", json=test_patient_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_patient_data["email"]
    assert data["name"] == test_patient_data["name"]
    assert "id" in data
    print(data)
    assert "password" not in data

def test_register_duplicate_email(test_patient_data):
    client.post("/api/v1/auth/register/patient", json=test_patient_data)
    response = client.post("/api/v1/auth/register/patient", json=test_patient_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"

def test_login_success(test_patient_data):
    client.post("/api/v1/auth/register/patient", json=test_patient_data)
    
    login_data = {
        "email": test_patient_data["email"],
        "password": test_patient_data["password"]
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure(test_patient_data):
    client.post("/api/v1/auth/register/patient", json=test_patient_data)
    
    login_data = {
        "email": test_patient_data["email"],
        "password": "wrongpassword"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401

def test_create_appointment_success(patient_token, test_patient_data, doctor_token):
    headers_doc = {"Authorization": f"Bearer {doctor_token}"}
    start_time = datetime.now() + timedelta(days=2)
    day_of_week = start_time.weekday()
    
    wh_res = client.post("/api/v1/working-hours/", json={
        "day": day_of_week,
        "start": "08:00",
        "end": "18:00"
    }, headers=headers_doc)
    assert wh_res.status_code == 200

    headers_pat = {"Authorization": f"Bearer {patient_token}"}
    appt_start = start_time.replace(hour=10, minute=0, second=0, microsecond=0)
    appt_end = appt_start + timedelta(minutes=30)
    
    payload = {
        "doctor_id": test_patient_data["doctor_id"],
        "start": appt_start.isoformat(),
        "end": appt_end.isoformat()
    }
    
    response = client.post("/api/v1/appointments/", json=payload, headers=headers_pat)
    assert response.status_code == 200
    assert response.json()["id"] is not None

def test_create_appointment_less_than_24h(patient_token, test_patient_data):
    headers = {"Authorization": f"Bearer {patient_token}"}
    appt_start = datetime.now() + timedelta(hours=2)
    appt_end = appt_start + timedelta(minutes=30)
    
    payload = {
        "doctor_id": test_patient_data["doctor_id"],
        "start": appt_start.isoformat(),
        "end": appt_end.isoformat()
    }
    
    response = client.post("/api/v1/appointments/", json=payload, headers=headers)
    assert response.status_code == 400
    assert "Must be 24h before" in response.json()["detail"]

def test_cancel_appointment_late(patient_token, test_patient_data, doctor_token):
    headers_doc = {"Authorization": f"Bearer {doctor_token}"}
    start_time = datetime.now() + timedelta(days=1)
    client.post("/api/v1/working-hours/", json={
        "day": start_time.weekday(),
        "start": "08:00", "end": "18:00"
    }, headers=headers_doc)

    headers_pat = {"Authorization": f"Bearer {patient_token}"}
    appt_start = datetime.now() + timedelta(hours=26)
    appt_end = appt_start + timedelta(minutes=30)
    
    res = client.post("/api/v1/appointments/", json={
        "doctor_id": test_patient_data["doctor_id"],
        "start": appt_start.isoformat(),
        "end": appt_end.isoformat()
    }, headers=headers_pat)
    
    assert res.status_code == 200
    appt_id = res.json()["id"]
    
    cancel_res = client.delete(f"/api/v1/appointments/{appt_id}", headers=headers_pat)
    assert cancel_res.status_code == 200
