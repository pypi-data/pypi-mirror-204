import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sm3(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("sm3", self, **kwargs).digest()
