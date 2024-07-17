#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def add_user(self, email: str, hashed_password: str):
        """ Adds a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs):
        """ finds a user by keywords
        """
        session = self._session
        results = session.query(User).filter_by(**kwargs)
        if len(list(results)) == 0:
            raise NoResultFound
        return results[0]

    def update_user(self, user_id: int, **kwargs):
        """ Updates a user with the values in the keyword args
        """
        session = self._session
        try:
            user = session.query(User).filter(User.id == user_id).first()
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
        except Exception:
            raise ValueError
