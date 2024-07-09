#!/usr/bin/env python3
""" The auth module
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ The Authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks if a path requires authentication"""
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        normal_path = path.rstrip('/')
        for path in excluded_paths:
            normal_pattern = path.rstrip('/')
            if fnmatch.fnmatch(normal_path, normal_pattern):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """retrieves the authorization header from the request"""
        if request is None:
            return None
        auth_key = request.headers.get('Authorization')
        if auth_key is None:
            return None
        return auth_key

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None
