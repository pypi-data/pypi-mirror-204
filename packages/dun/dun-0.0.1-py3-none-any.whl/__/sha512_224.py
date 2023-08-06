import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha512_224(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("sha512_224", self, **kwargs).digest()
