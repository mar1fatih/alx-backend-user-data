#!/usr/bin/env python3
""" API authentication """
from flask import request
from typing import List, TypeVar


class Auth():
    """ class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not in the list excluded_paths """
        if not path:
            return True
        if not excluded_paths:
            return True
        if len(excluded_paths) == 0:
            return True
        if path[-1] == '/':
            if path in excluded_paths:
                return False
            else:
                return True
        else:
            if path + '/' in excluded_paths:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """  return the value of the header request Authorization """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
