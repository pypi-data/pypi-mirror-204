from __.base import Signer, io, silent, to_bytes
from __.field import pf
from __.secp256k1 import secp256k1
from __.sha256 import sha256
from __.utils import bytes_to_int, f_, flatten, g_f, m_, random_znz, split_by


class ecdsa(Signer):
    @property
    def def_curve(self):
        return secp256k1()

    @property
    def def_hasher(self):
        return sha256()

    @io(data="msg")
    @silent
    def sign(self, privkey, msg=None, **kwargs):
        # privkey to field element
        privkey = to_bytes(privkey)
        e = pf(self.curve.n)(privkey)

        # hashed message, H(M) to field element
        z = pf(self.curve.n)(self.hasher.hash(data=self))

        # construct R-point: r == x-coordinate of R
        k = random_znz(self.curve.n)
        R = self.curve.kG(k)
        r = pf(self.curve.n)(R.x.e)

        # return signature (r,s)
        s = (z + r * e) / k
        if not s:
            return self.sign(privkey, msg=msg, **kwargs)
        else:
            return r.eb + s.eb

    @io(data="sig", lift=0)
    @silent
    def verify(self, pubkey, msg, sig=None, **kwargs):
        pubkey = to_bytes(pubkey)
        # bytes-pubkey to a point on elliptic curve
        b = self.curve.bytes
        x, y = bytes_to_int(pubkey[:b]), bytes_to_int(pubkey[b:])
        P = self.curve.ap(x, y)

        # split signature (r,s) into each field element
        r, s = self[:b], self[b:]
        r = pf(self.curve.n)(r)
        s = pf(self.curve.n)(s)

        # hashed message, H(M) to field element
        z = pf(self.curve.n)(self.hasher.hash(data=msg))

        # reconstruct R-point from signature and pubkey
        G = self.curve.G
        R = (z / s) * G + (r / s) * P
        return r.e == R.x.e

    @silent
    def load(self, data, op=None):
        def ser(o):
            s = self.curve.bytes
            l = f_(self.lifter, op=op)
            return g_f(b"".join, m_(g_f(l, f_(to_bytes, size=s))), list, flatten)(o)

        return super().load(data, ser=ser)

    @silent
    def unload(self, op=None):
        s = self.curve.bytes
        u = f_(self.dumper, op=op)
        return g_f(tuple, m_(g_f(u, bytes)), f_(split_by, self))([s])
