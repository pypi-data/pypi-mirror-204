import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class whirlpool(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("whirlpool", self, **kwargs).digest()
