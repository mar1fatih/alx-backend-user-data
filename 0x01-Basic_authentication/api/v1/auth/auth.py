#!/usr/bin/env python3
""" API authentication """
from flask import request
from typing import List, TypeVar


class Auth():
    """ class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        if not path:
            return True
        if not excluded_paths and len(excluded_paths) == 0:
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
        """ returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
