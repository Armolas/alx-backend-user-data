#!/usr/bin/env python3
""" The authentication module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union, TypeVar
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

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """ retrieves a user from the session id
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys a user session
        """
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates a password reset token
        """
        if not email:
            return None
        reset_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates a user password
        """
        if not reset_token or not password:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_pwd = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=new_pwd,
                    reset_token=None
                    )
            return None
        except Exception as e:
            raise ValueError
