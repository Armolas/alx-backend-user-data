#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


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
        """ Adds a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ finds a user by keywords
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates a user with the values in the keyword args
        """
        try:
            user = self._session.query(User).filter_by(id=user_id).first()
            keys = ['hashed_password', 'email', 'session_id', 'reset_token']
            for key, value in kwargs.items():
                if key not in keys:
                    raise ValueError
                setattr(user, key, value)
            self._session.commit()
            return None
        except Exception as e:
            raise ValueError
