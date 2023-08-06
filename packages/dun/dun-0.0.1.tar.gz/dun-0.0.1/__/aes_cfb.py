from Crypto.Cipher import AES

from __.base import Encryptor, io, silent, to_bytes
from __.sha256 import sha256
from __.utils import pad, random_bytes, unpad


class aes_cfb(Encryptor):
    @io()
    @silent
    def encrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        key = len(key) == 32 and key or sha256().hash(data=key)
        iv = random_bytes(16)
        cipher = AES.new(key, AES.MODE_CFB, iv, **kwargs)
        return iv + cipher.encrypt(pad(self))

    @io()
    @silent
    def decrypt(self, key, data=None, **kwargs):
        key = to_bytes(key)
        key = len(key) == 32 and key or sha256().hash(data=key)
        iv, data = self[:16], self[16:]
        cipher = AES.new(key, AES.MODE_CFB, iv, **kwargs)
        return unpad(cipher.decrypt(data))
