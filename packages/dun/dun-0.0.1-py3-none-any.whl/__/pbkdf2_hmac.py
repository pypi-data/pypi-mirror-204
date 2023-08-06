import hashlib

from __.base import Hasher, io, nilbyte_p, silent, to_bytes
from __.utils import random_bytes


class pbkdf2_hmac(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, hash_fn="sha512", salt=None, itr=2048, data=None, **kwargs):
        salt = to_bytes(salt) or random_bytes(16)
        return hashlib.pbkdf2_hmac(hash_fn, self, salt, itr, **kwargs)
