#!/usr/bin/env python3
""" The authentication module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ hashes a password into a salted hash bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ generates a unique id
    """
    uid = uuid.uuid4()
    return str(uid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initializes a new db
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a new user to the db
        """
        if not email or not password:
            return
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ validates user credentials
        """
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates a new user session
        """
        if not email:
            return None
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> None:
        """ retrieves a user from the session id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=sessio_id)
            return user
        except Exception as e:
            return None
