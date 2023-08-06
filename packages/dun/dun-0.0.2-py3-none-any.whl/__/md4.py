import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class md4(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("md4", self, **kwargs).digest()
