import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class md5_sha1(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.new("md5-sha1", self, **kwargs).digest()
