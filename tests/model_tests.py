import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from back_end.models import *


@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_validate_user_signup_success():
    errors = validate_user_signup("BrayanCova", "brayan@gmail.com", "HehSecure3")
    assert errors is None


def test_validate_user_signup_email_error():
    errors = validate_user_signup("BrayanCova", "notanemail", "HehSecure3")
    assert errors == ['Please enter a valid email']


def test_validate_user_signup_password_error():
    errors = validate_user_signup("BrayanCova", "brayan@gmail.com", "pass")
    assert errors == ['Password MUST be at least 8 characters long, 1 letter, and 1 number']


def test_validate_user_signup_empty_error():
    errors = validate_user_signup("", "", "")
    assert errors == ['Username must be at least 5 characters in length', 'Email is required', 'Password is required']


def test_validate_user_login():
    print("")


def test_check_user_exists():
    print("")


def test_get_user():
    print("")
