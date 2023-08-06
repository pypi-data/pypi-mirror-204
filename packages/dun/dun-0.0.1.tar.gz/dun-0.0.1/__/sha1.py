import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha1(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha1(self, **kwargs).digest()
