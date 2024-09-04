#!/usr/bin/env python3
""" BasicAuth class """
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
