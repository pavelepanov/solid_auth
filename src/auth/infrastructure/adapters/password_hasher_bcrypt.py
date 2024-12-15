# pylint: disable=C0301 (line-too-long)

import base64
import hashlib
import hmac

import bcrypt

from auth.domain.user.ports.password_hasher import PasswordHasher
from auth.domain.user.value_objects import RawPassword
from auth.infrastructure.types import PasswordPepper


class BcryptPasswordHasher(PasswordHasher):
    def __init__(self, pepper: PasswordPepper):
        self._pepper = pepper

    def hash(self, raw_password: RawPassword) -> bytes:
        base64_hmac_password: bytes = self._add_pepper(raw_password, self._pepper)
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(base64_hmac_password, salt)

    @staticmethod
    def _add_pepper(raw_password: RawPassword, pepper: str) -> bytes:
        hmac_password: bytes = hmac.new(
            key=pepper.encode(),
            msg=raw_password.value.encode(),
            digestmod=hashlib.sha256,
        ).digest()
        return base64.b64encode(hmac_password)

    def verify(self, *, raw_password: RawPassword, hashed_password: bytes) -> bool:
        base64_hmac_password: bytes = self._add_pepper(raw_password, self._pepper)
        return bcrypt.checkpw(base64_hmac_password, hashed_password)
    