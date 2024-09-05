#!/usr/bin/env python3
"""session auth"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """ SessionAuth class """
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if not user_id or type(user_id) is not str:
            return None
        session_id = uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
