import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class md5(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.md5(self, **kwargs).digest()
