#!/usr/bin/env python3
"""auth encryption"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """hash the password and save the user to the database"""
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound or InvalidRequestError:
            pss = _hash_password(password)
            return self._db.add_user(email, pss)
        if usr:
            raise ValueError("User {} already exists".format(email))
