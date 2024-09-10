#!/usr/bin/env python3
"""auth encryption"""
import bcrypt


def _hash_password(password):
    """returns a hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
