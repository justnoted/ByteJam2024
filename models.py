from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///supply_tracker.db')

Base = declarative_base()

Session = sessionmaker(bind=engine)


class user:
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


Base.metadata.create_all(engine)