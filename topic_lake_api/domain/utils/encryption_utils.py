import binascii
import hashlib
import os

_salt_length = 64


def _hash_password(password: str, salt: bytes) -> bytes:
    return binascii.hexlify(
        hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100_000)
    )


def hash_password(password: str) -> str:
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    return (salt + _hash_password(password, salt)).decode('ascii')


def check_password(stored_password: str, provided_password: str) -> bool:
    salt = stored_password[:64]
    stored_password = stored_password[64:]

    return stored_password == _hash_password(provided_password, salt.encode('ascii')).decode('ascii')
