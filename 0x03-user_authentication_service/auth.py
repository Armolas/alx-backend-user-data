#!/usr/bin/env python3
""" The authentication module
"""
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(self, password: str) -> bytes:
    """ hashes a password into a salted hash bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initializes a new db
        """
        self._db = DB()

    def register_user(self, email, password):
        """ registers a new user to the db
        """
        session = self._db._session
        user = session.query(User).filter_by(email=email).one_or_none()
        if user is not None:
            raise ValueError(f"User {email} already exists")
        hashed_pwd = _hash_password(password)
        user = self._db.add_user(email, hashed_pwd)
        return user

    def valid_login(self, email, password):
        """ validates user credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except Exception:
            return False

    def _generate_uuid(self):
        """ generates a unique id
        """
        uid = uuid.uuid4()
        return str(uid)

    def create_session(self, email):
        """ creates a new user session
        """
        session_id = self._generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except Exception:
            return None
