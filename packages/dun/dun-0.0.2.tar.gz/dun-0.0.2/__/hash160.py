from __.base import Hasher, io, nilbyte_p, silent
from __.ripemd160 import ripemd160
from __.sha256 import sha256


class hash160(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return ripemd160().hash(data=sha256().hash(data=self, **kwargs))
