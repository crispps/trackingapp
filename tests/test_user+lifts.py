import pytest

from lifts import Lift

from user import User


def load_lift_data_stub(path):
    return {"bench press": {"username1": [{"date": "2026-02-03", "weight": "125", "sets": "1", "reps": "1", "rpe": "7"},
                                          {"date": "2026-02-03", "weight": "117.5", "sets": "3", "reps": "3",
                                           "rpe": "8"}]}, "squat": {
        "username1": [{"date": "2026-02-02", "weight": "175", "sets": "3", "reps": "3", "rpe": "7"},
                      {"date": "2026-02-02", "weight": "200", "sets": "1", "reps": "1", "rpe": "8"},
                      {"date": "2026-02-20", "weight": "197.5", "sets": "1", "reps": "1", "rpe": "8.5"}]}}


@pytest.fixture
def user1(monkeypatch):
    monkeypatch.setattr(Lift, "load_lift_data", load_lift_data_stub)
    user = User("username1", "")
    lift = Lift("")

    lift.data = load_lift_data_stub("")
    user.data = lift

    return user


def test_create_user_assign_username_stub(user1):
    assert user1.username == "username1"


def test_create_lifts_assign_data(user1):
    assert user1.data.data == load_lift_data_stub("")


def test_user_add_data(monkeypatch, user1):
    data = {"lift": "bench press", "date": "2000-01-01", "weight": "120", "sets": "2", "reps": "3", "rpe": "8"}
    lift_name = data.get("lift")
    monkeypatch.setattr(Lift, "dump_data", lambda x: None)
    user1.add_data(data)
    assert data in user1.data.data[lift_name][user1.username]


def test_user_lift_exists_unit(user1):
    assert user1.lift_exists("bench press")


def test_user_get_lifts_unit(user1):
    assert user1.data.get_lifts() == ["bench press", "squat"]


def test_user_lift_history_unit(user1):
    bench_history = load_lift_data_stub("")["bench press"][user1.username]
    assert user1.lift_history("bench press") == bench_history


def test_user_create_lift_happy_unit(monkeypatch, user1):
    monkeypatch.setattr(Lift, "dump_data", lambda x: None)
    lift_name = "deadlift"
    created = user1.add_lift(lift_name)
    assert ((lift_name in list(user1.data.data.keys())) and created)


def test_user_create_lift_sad_unit(monkeypatch, user1):
    monkeypatch.setattr(Lift, "dump_data", lambda x: None)
    lift_name = "squat"
    create = user1.add_lift(lift_name)
    assert ((lift_name in list(user1.data.data.keys())) and not create)
