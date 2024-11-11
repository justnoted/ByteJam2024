from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import re

engine = create_engine('sqlite:///shrimpnews.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class CustomNews(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')


def validate_user_signup(username, email, password):
    errors = []

    if check_if_user_exists(username):
        errors.append(f"`{username}` already exists. Please log in or use a different username")
        return errors

    errors.append("Username must be at least 5 characters in length") if len(username) < 5 else None

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    pass_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"  # TODO: Revise regex, not working

    errors.append("Email is required") if email.strip() == "" else errors.append("Please enter a valid email") if not re.fullmatch(email_regex, email) else None
    errors.append("Password is required") if password.strip() == "" else errors.append("Password MUST be 6-20 long, 1 UPPERCASE, 1 lowercase, and 1 special symbol") if re.match(pass_regex, password) else None

    return errors if errors else None


def validate_user_login(username, password):
    errors = []

    if check_if_user_exists(username):
        user = get_user_with_username(username)
        if user.password == password:
            return None
        errors.append("Username and password do not match. Please try again")
    else:
        errors.append(f"\"{username}\" does not exist. Create an account today") if username.strip() != "" else errors.append("Username and password are required to login")

    return errors


def check_if_user_exists(username):
    return bool(session.query(User).filter_by(username=username).first()) if username.strip() != "" else False


def get_user_with_username(username):
    return session.query(User).filter_by(username=username).first()


def get_today_decade():
    year = datetime.now().year
    return year - (year % 10)


Base.metadata.create_all(engine)