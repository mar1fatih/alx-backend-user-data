#!/usr/bin/env python3
""" BasicAuth class """
import base64
from api.v1.auth.auth import Auth


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
