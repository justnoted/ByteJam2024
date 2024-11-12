import pytest

from back_end.models import *

@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
def test_check_user_exists(test_session):
    user = User(username="testuser", email="test@example.com", password="TestPassword123!")
    test_session.add(user)
    test_session.commit()

    assert check_if_user_exists(test_session, "testuser")
    assert not check_if_user_exists(test_session, "nonexistentuser")

def test_get_user(test_session):
    user = User(username="testuser", email="test@example.com", password="TestPassword123!")
    test_session.add(user)
    test_session.commit()

    retrieved_user = get_user_with_username(test_session, "testuser")
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.password == "TestPassword123!"

def test_get_today_decade():
    assert get_today_decade() == datetime.now().year - (datetime.now().year % 10)
