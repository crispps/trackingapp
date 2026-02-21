import pytest
import process as pc


# monkey patch functions
def mock_get_user_list():
    return ["username1", "username2"]


def test_check_return_path_unit():
    assert pc.get_users_path() == "data/users.json"


def test_check_username_exists_unit(monkeypatch):
    monkeypatch.setattr(pc, "get_user_list", mock_get_user_list)
    assert pc.check_username_exists("username2")


def test_check_username_doesnt_exist_unit(monkeypatch):
    monkeypatch.setattr(pc, "get_user_list", mock_get_user_list)
    assert not pc.check_username_exists("user")


def test_login_happy_path(monkeypatch):
    monkeypatch.setattr(pc, "check_username_exists", lambda x: True)
    assert pc.login("username")


def test_login_sad_path(monkeypatch):
    monkeypatch.setattr(pc, "check_username_exists", lambda x: False)
    assert not pc.login("username")


def test_login_creates_user_object(monkeypatch):
    monkeypatch.setattr(pc, "check_username_exists", lambda x: True)
    pc.login("username1")
    assert pc.user.username == "username1"


def test_login_doesnt_create_user_object(monkeypatch):
    monkeypatch.setattr(pc, "check_username_exists", lambda x: False)
    pc.login("username2")
    assert pc.user is None
