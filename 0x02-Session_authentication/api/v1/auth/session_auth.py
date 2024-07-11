#!/usr/bin/env python3
"""The Session Authentication Module"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ The session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session id for the user """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        SessionAuth.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrieves a user based on the session id """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ returns a user instance """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ destroys a user session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        try:
            del SessionAuth.user_id_by_session_id[session_id]
        except Exception:
            return False
        return True
