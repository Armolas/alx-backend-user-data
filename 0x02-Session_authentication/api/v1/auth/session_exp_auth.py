#!/usr/bin/env python3
""" The timed session authentication
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ The Expiring Session Authentication Class
    """
    def __init__(self):
        """ The instance init method
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {}
        session_dictionary["user_id"] = user_id
        session_dictionary["created_at"] = datetime.now()
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ gets the user id from the session_id
        """
        if session_id is None:
            return None
        session_dictionary = SessionAuth.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        duration = timedelta(seconds=self.session_duration)
        if created_at + duration < datetime.now():
            return None
        return session_dictionary.get("user_id")
