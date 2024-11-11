import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import *

@pytest.fixture(scope='module')
def test_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_validate_user_signup():
    print("")


def test_validate_user_login():
    print("")


def test_check_user_exists():
    print("")


def test_get_user():
    print("")


def test_get_today_decade():
    datetime.now().year