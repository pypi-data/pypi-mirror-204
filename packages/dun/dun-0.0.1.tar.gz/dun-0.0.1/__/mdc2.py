import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class mdc2(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("mdc2", self, **kwargs).digest()
