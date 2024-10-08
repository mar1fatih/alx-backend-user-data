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

    def create_session(self, email: str) -> str:
        """store uuid in the database as session_id, and return it"""
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound or InvalidRequestError:
            return None
        _id = _generate_uuid()
        setattr(usr, 'session_id', _id)
        return _id

    def get_user_from_session_id(self, session_id: str) -> User:
        """returns the corresponding User from session_id"""
        if not session_id:
            return None
        try:
            usr = self._db.find_user_by(session_id=session_id)
            if not usr:
                return None
            return usr
        except NoResultFound or InvalidRequestError:
            return None

    def destroy_session(self, user_id: int) -> None:
        """updates the corresponding user’s session ID to None"""
        try:
            usr = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound or InvalidRequestError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generate a UUID and update the user’s reset_token"""
        try:
            usr = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(usr.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update user's password"""
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
            hached_pass = _hash_password(password)
            self._db.update_user(usr.id, hashed_password=hached_pass,
                                 reset_token=None)
            return None
        except Exception:
            raise ValueError
