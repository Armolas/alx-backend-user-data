#!/usr/bin/env python3
'''encrypt password'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''generatates a salted hashed password'''
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return hashed_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''validates an hashed password'''
    return bcrypt.checkpw(password.encode(), hashed_password)
