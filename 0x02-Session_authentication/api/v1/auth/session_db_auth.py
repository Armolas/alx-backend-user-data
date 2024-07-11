#!/usr/bin/env python3
""" The DB user session module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ The DB session class
    """
    def create_session(self, user_id=None):
        """ creates new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user id from session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if len(sessions) == 0:
            return None
        session = sessions[0]
        created_at = session.created_at
        duration = timedelta(seconds=self.session_duration)
        if created_at + duration < datetime.utcnow():
            session.remove()
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """ deletes a user session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if len(sessions) == 0:
            return False
        session = sessions[0]
        session.remove()
        return True
