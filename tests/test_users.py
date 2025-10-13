from app import schemas 
import pytest
from jose import jwt
from app.config import settings


# def test_root(client):
#     response = client.get("/")
#     print(response.json().get("message"))
#     assert response.json().get("message") == "gigga nigga"
#     assert response.status_code == 200

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"name": "testuser23", "email": "xQ2Xe@exampl23e.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "xQ2Xe@exampl23e.com"
    assert response.status_code == 201



def test_login_user(client, test_user):
    
    response = client.post(
        "/login",
        data={"username": test_user["email"],"password": test_user["password"]}
    )
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@example.com", "password123", 403),
    ("xQ2Xe@example.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("xQ2Xe@example.com", None, 422)
    
])
def test_incorrect_login(client, test_user, email, password, status_code):
    
    response = client.post(
        "/login",
        data={"username": email,"password": password}
    )
    assert response.status_code == status_code



