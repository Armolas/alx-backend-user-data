#!/usr/bin/env python3
""" The basic auth module
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """ The Basic Authentication Class """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        auth = authorization_header.split(' ')[1].strip()
        return auth

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        that returns the decoded value of a
        Base64 string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded = decoded_bytes.decode('utf-8')
        except Exception:
            return None
        return decoded

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        return (credentials[0], credentials[1])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        from models.user import User
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if len(users) == 0:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves the User instance for a request
        """
        auth = self.authorization_header(request)
        b64auth = self.extract_base64_authorization_header(auth)
        authStr = self.decode_base64_authorization_header(b64auth)
        user_credential = self.extract_user_credentials(authStr)
        email = user_credential[0]
        pwd = user_credential[1]
        user = self.user_object_from_credentials(email, pwd)
        return user
