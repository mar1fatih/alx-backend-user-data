#!/usr/bin/env python3
""" BasicAuth class """
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract the base64 from authorization_header"""
        if not authorization_header or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode by base64"""
        b64_header = base64_authorization_header
        if not b64_header or type(b64_header) is not str:
            return None
        try:
            b64_header = base64.b64decode(b64_header).decode('utf-8')
        except Exception:
            b64_header = None
        return b64_header

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password from the decoded value"""
        b64 = decoded_base64_authorization_header
        if not b64:
            return (None, None)
        if type(b64) is not str:
            return (None, None)
        b64 = decoded_base64_authorization_header.split(':')
        if len(b64) < 2:
            return (None, None)
        else:
            email = b64[0]
            b64.pop(0)
            password = ':'.join(b64)
        return (email, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """return User instance based on email and password"""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        user = User()
        last_user = user.search({'email': user_email})
        if not last_user:
            return None
        for user in last_user:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """authorize request and return user"""
        if not request:
            return None
        header = request.headers['Authorization']
        auth = self.extract_base64_authorization_header(header)
        dcd = self.decode_base64_authorization_header(auth)
        user = self.extract_user_credentials(dcd)
        user_email = user[0]
        user_pwd = user[1]
         return self.user_object_from_credentials(user_email, user_pwd)
