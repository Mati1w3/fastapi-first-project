import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = list(map(validate, res.json()))
    posts_sorted = sorted(posts_map, key=lambda post: post.Post.id)
    
    # -------------------------------------------------------------------------
    
    assert len(posts_map) == len(test_posts)
    assert res.status_code == 200
    
    assert posts_sorted[0].Post.id == test_posts[0].id
    assert posts_sorted[0].Post.title == test_posts[0].title
    assert posts_sorted[0].Post.content == test_posts[0].content
    assert posts_sorted[0].Post.published == test_posts[0].published

    assert posts_sorted[0].likes == 0
    assert posts_sorted[0].comments_count == 0
    assert posts_sorted[0].comments == []


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.published == test_posts[0].published



@pytest.mark.parametrize("title, content, published", [
    ("title", "content", True),
    ("title", "content", False),
    ("title", "", True),
    ("", "content", True),
    ("title", "", False),
    ("", "content", False),


])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    assert res.status_code == 201

    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_unauthorized_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "title", "content": "content", "published": True})

    assert res.status_code == 401
@pytest.mark.parametrize("title, content, published", [
    ("title", "content", True),
    ("title", "content", False),
    ("title", "", True),
    ("", "content", True),
    ("title", "", False),
    ("", "content", False),
])

def test_create_post_unauthorized(client, test_user, test_posts, title, content, published):
    res = client.post("/posts/", json={"title": title, "content": content, "published": published})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401



def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/8888")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts, test_user2):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")


    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put("/posts/8888", json=data)

    assert res.status_code == 404