from __.base import Encryptor, io, silent, to_bytes
from __.sha256 import sha256


class rsa(Encryptor):
    @io()
    @silent
    def encrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        pass

    @io()
    @silent
    def decrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        pass
