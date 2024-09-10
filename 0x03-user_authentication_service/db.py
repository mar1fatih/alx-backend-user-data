#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns a User object"""
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()
        return usr

    def find_user_by(self, **kwargs) -> User:
        """ returns the first row found in the users table"""
        for key, value in kwargs.items():
            if hasattr(User, key):
                usr = self._session.query(
                        User).filter_by(**{key: value}).first()
                if usr:
                    return usr
                else:
                    raise NoResultFound
            else:
                raise InvalidRequestError

    def update_user(self, user_id: str, **kwargs) -> None:
        """update the user’s attributes as passed
        in the method’s arguments"""
        try:
            usr = self.find_user_by(id=user_id)
            for k, v in kwargs.items():
                setattr(usr, k, v)
            self._session.commit()
        except NoResultFound or InvalidRequestError:
            raise ValueError
