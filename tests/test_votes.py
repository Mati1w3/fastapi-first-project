import pytest

from app import models

@pytest.fixture(scope="function")
def test_votes(session, test_posts, test_user, test_user2):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    return session


def test_vote_on_post(authorized_client, test_posts, test_user, test_user2):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 201


def test_vote_twice_on_post(authorized_client, test_posts, test_votes):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409


def test_remove_vote(authorized_client, test_posts, test_votes):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 201

def test_remove_vote_non_exist(authorized_client, test_posts, test_user, test_user2):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 404

def test_vote_post_non_exist(authorized_client, test_posts, test_user, test_user2):
    res = authorized_client.post("/vote/", json={"post_id": 888888, "dir": 1})

    assert res.status_code == 404

def test_unauthorized_user_vote(client, test_posts, test_user, test_user2):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 401

def test_unauthorized_user_delete_vote(client, test_posts, test_user, test_user2):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 401
