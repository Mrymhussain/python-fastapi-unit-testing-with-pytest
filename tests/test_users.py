from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import UserModel
from tests.lib import login


def test_register_user(test_app: TestClient, override_get_db):
    user_data = {
        "username": "maryamtest",
        "email": "maryamtest@example.com",
        "password": "password123"
    }

    response = test_app.post("/api/register", json=user_data)

    assert response.status_code == 201
    assert "token" in response.json()
    assert response.json()["message"] == "Login successful"


def test_login_user(test_app: TestClient, test_db: Session):
    user = UserModel(
        username="testlogin",
        email="testlogin@example.com"
    )

    user.set_password("password123")

    test_db.add(user)
    test_db.commit()

    response = test_app.post(
        "/api/login",
        json={
            "username": "testlogin",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert "token" in response.json()
    assert response.json()["message"] == "Login successful"


def test_current_user(test_app: TestClient, test_db: Session):
    user = UserModel(
        username="currentuser",
        email="currentuser@example.com"
    )

    user.set_password("password123")

    test_db.add(user)
    test_db.commit()

    headers = login(
        test_app,
        "currentuser",
        "password123"
    )

    response = test_app.get(
        "/api/current_user",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["username"] == "currentuser"
    assert response.json()["email"] == "currentuser@example.com"