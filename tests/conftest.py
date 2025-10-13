from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import Base, get_db
from app.config import settings
from app.oauth2 import create_access_token
from . import models

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:4422@localhost:5432/testdb'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    
@pytest.fixture
def test_user(client):
    user_data = {
        "name": "testuser",
        "email": "xQ2Xe@example.com",
        "password": "password123"
    }
    result = client.post("/users/", json=user_data)
    assert result.status_code == 201
    new_user = result.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"], "user_name": test_user["name"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"]
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user["id"]
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user["id"]
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2["id"]
        }
    ]
    def create_post(post):
        new_post = models.Post(**post)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
    posts = list(map(create_post, posts_data))
    return posts