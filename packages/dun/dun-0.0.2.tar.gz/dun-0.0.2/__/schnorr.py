from __.base import Signer, io, silent, to_bytes
from __.field import pf
from __.secp256k1 import secp256k1
from __.sha256 import sha256
from __.utils import bytes_to_int, f_, flatten, g_f, m_, random_znz, split_by


class schnorr(Signer):
    curve = secp256k1()
    hasher = sha256()

    @io(data="msg")
    @silent
    def sign(self, privkey, msg=None, **kwargs):
        # privkey to field element
        privkey = to_bytes(privkey)
        x = pf(self.curve.n)(privkey)

        # construct R-point: r == x-coordinate of R
        k = random_znz(self.curve.n)
        R = self.curve.kG(k)
        r = pf(self.curve.n)(R.x.e)

        # pad-hashed message, H(r||M) to field element
        e = pf(self.curve.n)(self.hasher.hash(data=r.eb + self))

        # return signature (s,e)
        s = k - x * e
        if not s:
            return self.sign(privkey, msg=msg, **kwargs)
        else:
            return s.eb + e.eb

    @io(data="sig", lift=0)
    @silent
    def verify(self, pubkey, msg, sig=None, **kwargs):
        pubkey = to_bytes(pubkey)
        # bytes-pubkey to a point on elliptic curve
        b = self.curve.bytes
        x, y = bytes_to_int(pubkey[:b]), bytes_to_int(pubkey[b:])
        P = self.curve.ap(x, y)

        # split signature (s,e) into each field element
        s, e = self[:b], self[b:]
        s = pf(self.curve.n)(s)
        e = pf(self.curve.n)(e)

        # reconstruct R-point from signature and pubkey
        G = self.curve.G
        R = s * G + e * P
        r_v = pf(self.curve.n)(R.x.e)

        # reconstruct hashed message H(r_v||M) using r_v
        e_v = pf(self.curve.n)(self.hasher.hash(data=r_v.eb + to_bytes(msg)))
        return e.e == e_v.e

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
