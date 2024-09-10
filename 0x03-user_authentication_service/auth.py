#!/usr/bin/env python3
"""auth encryption"""
import bcrypt
import uuid
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid() -> str:
    """ return a string representation of a new UUID """
    return str(uuid.uuid4())

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

    def valid_login(self, email: str, password: str) -> bool:
        """ check the password return True or False."""
        try:
            usr = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), usr.hashed_password):
                return True
            else:
                return False
        except NoResultFound or InvalidRequestError:
            return False
