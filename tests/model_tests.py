import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import *

@pytest.fixture(scope='session')