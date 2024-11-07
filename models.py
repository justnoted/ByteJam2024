from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import re

engine = create_engine('sqlite:///shrimpnews.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()


class User:
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class CustomNews:
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')


def validate_user_signup(username, email, password):
    errors = []

    if username.strip() == "":
        check_user = bool(session.query(User).filter_by(username=username).first())
        if check_user:
            errors.append(f"`{username}` already exists. Please log in or use a different username.")
            return errors
        errors.append("Username must be at least 5 characters in length") if len(username) < 5 else None
    else:
        errors.append("Username is required.")

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    pass_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    errors.append("Email is required.") if email.strip() == "" else errors.append("Please enter a valid email") if not re.fullmatch(email_regex, email) else None
    errors.append("Password is required") if password.strip() == "" else errors.append("Password MUST be 6-20 long, 1 UPPERCASE, 1 lowercase, and 1 special symbol.") if re.search(pass_regex, password) else None

    return errors if errors else None


def validate_user_login(username, password):
    errors = []

    if username.strip() == "":
        check_user = bool(session.query(User).filter_by(username=username).first())
        if not check_user:
            errors.append(f"`{username}` does not exist. Create an account today! :)")
            return errors
        # TODO: Validate if password matches with input password. Use Username to match. Add encryption.


Base.metadata.create_all(engine)
