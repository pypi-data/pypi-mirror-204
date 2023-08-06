from __.base import Byteable, silent, to_bytes
from __.secp256k1 import secp256k1
from __.tonelli import sqrt_zpz
from __.utils import (
    bytes_to_int,
    f_,
    flatten,
    g_f,
    int_to_bytes,
    m_,
    split_by,
    status,
    usage,
)


def decompress_pubkey(pubkey, curve):
    """compressed-pubkey to uncompressed pubkey"""
    parity, x = map(bytes_to_int, (pubkey[1:], pubkey[1:]))
    parity -= 2
    y2 = (pow(x, 3, curve.p) + curve.a * x + curve.b) % curve.p

    # Get sqrt(y^2) over GF(p) use Tonelli-Shank's algorithm
    y = sqrt_zpz(y2, curve.p)

    # Or directly calculate using the property: a = x^((p+1)/4)  (when p=3 mod 4)
    # y = pow(y2, (curve.p + 1) // 4, curve.p)
    if y % 2 != parity:
        y = -y % curve.p
    return int_to_bytes(x, curve.bytes) + int_to_bytes(y, curve.bytes)


class keys(Byteable):
    def __repr__(self):
        return status(
            ("kind", "EC-key generator"), ("curve", self.curve), ("data", self)
        )

    @property
    def _(self):
        self.help()

    @property
    def curve(self):
        return getattr(self, "_curve", self.def_curve)

    def set_curve(self, curve=None):
        curve = curve or self.def_curve
        setattr(self, "_curve", curve)
        return self

    @property
    def def_curve(self):
        return secp256k1()

    def help(self):
        super().help()
        usage(
            self.help,
            self.set_curve,
            self.unload,
            self.privkey,
            self.pubkey,
            self.pair,
            header=f"{self.__class__.__name__}",
        )

    def privkey(self, privkey=None):
        if to_bytes(privkey):
            if not len(privkey) == self.curve.bytes:
                raise ValueError(f"Invalid privkey: {privkey}")
            return super().load(privkey)
        else:
            return self.rand(self.curve.bytes)

    def pubkey(self, privkey=None, compressed=False):
        privkey = privkey or self
        priv = self.privkey(privkey)
        pub = self.curve.kG(priv.decimal()).to_bytes(compressed)
        return super().load(pub)

    def pair(self, privkey=None, compressed=False):
        privkey = privkey or self
        priv = self.privkey(privkey)
        pub = self.pubkey(priv, compressed)
        return super().load(priv + pub)

    @silent
    def load(self, data, op=None):
        def ser(o):
            s = self.curve.bytes
            l = f_(self.lifter, op=op)
            b = g_f(b"".join, m_(g_f(l, f_(to_bytes, size=s))), list, flatten)(o)
            if len(b) == 2 * s + 1:
                priv, pub = b[:s], b[s:]
                return priv + decompress_pubkey(pub, self.curve)
            elif len(b) == s + 1:
                return decompress_pubkey(b, self.curve)
            else:
                return b

        return super().load(data, ser=ser).set_curve(self.curve)

    @silent
    def unload(self, op=None):
        s = self.curve.bytes
        u = f_(self.dumper, op=op)
        f = g_f(tuple, m_(g_f(u, bytes)), f_(split_by, self))

        # priv + pub
        if self.length() == 3 * s:
            if op == "decimal":
                return f([s, 2 * s])
            else:
                return f([s])

        # priv + compressed-pub
        elif self.length() == 2 * s + 1:
            if op == "decimal":
                return f([s, s + 1])
            else:
                return f([s])

        # pub only
        elif self.length() == 2 * s:
            return f([s])

        # compressed-pub only
        elif self.length() == s + 1:
            return f([1])

        # otherwise
        else:
            return f([])[0]
