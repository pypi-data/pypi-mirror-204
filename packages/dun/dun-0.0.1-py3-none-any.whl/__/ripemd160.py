import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class ripemd160(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("ripemd160", self).digest()
