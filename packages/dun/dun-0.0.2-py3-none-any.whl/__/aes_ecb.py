from Crypto.Cipher import AES

from __.base import Encryptor, io, silent, to_bytes
from __.sha256 import sha256
from __.utils import pad, unpad


class aes_ecb(Encryptor):
    @io()
    @silent
    def encrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        key = len(key) == 32 and key or sha256().hash(data=key)
        cipher = AES.new(key, AES.MODE_ECB, **kwargs)
        return cipher.encrypt(pad(self))

    @io()
    @silent
    def decrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        key = len(key) == 32 and key or sha256().hash(data=key)
        cipher = AES.new(key, AES.MODE_ECB, **kwargs)
        return unpad(cipher.decrypt(self))
