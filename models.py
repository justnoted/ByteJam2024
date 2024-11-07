from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User:
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



class CustomNews:
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')


Base.metadata.create_all(engine)