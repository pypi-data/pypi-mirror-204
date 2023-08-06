import operator
import secrets
from functools import reduce

from __.base import Encryptor, io, silent, to_bytes
from __.field import evalpoly, recip
from __.utils import f_, flatten, flip, g_f, int_to_bytes, m_, split_by, status, usage


def lagrange_interpol(p, x, xs, ys):
    """Lagrange interpolation
    L(x) = Sum_{j=0}^{k} yj lj(x)
    lj(x) = TT_{0 <= m <=k; m != j} (x - xm) / (xj - xm)
    """

    def TT(x):
        return reduce(operator.mul, x, 1)

    def Os(x, i):
        return x[:i] + x[i + 1 :]

    k = len(xs)
    if k != len(set(xs)):
        raise ValueError("All points of shares should be unique.")

    nums = [TT(x - o for o in Os(xs, i)) for i in range(k)]
    dens = [TT(xs[i] - o for o in Os(xs, i)) for i in range(k)]
    num = sum((ys[i] * ((nums[i] * recip(dens[i], p)) % p)) % p for i in range(k))
    return num % p


class sss(Encryptor):
    """Shamir secret sharing (SSS)
    Maximum length of available secret depends on the size of prime used.

    A prime field from ellptic curve(secp256k1), where p = 2^256 - 2^32 - 977 or
    p = 115792089237316195423570985008687907853269984665640564039457584007908834671663

    Use well-known list of primes for encoding much longer secret.
    For example, Mersenne primes (Mp=2^p -1), where p = {..,127, 521, 607, 1279, 2203,..}.
    When p = 1279 (below, 386 digits) of prime can encode almost 1279 bits (or 160 bytes).
    p = 10407932194664399081925240327364085538615262247266704805319112350403608059673360298012239441732324184842421613954281007791383566248323464908139906605677320762924129509389220345773183349661583550472959420547689811211693677147548478866962501384438260291732348885311160828538416585028255604666224831890918801847068222203140521026698435488732958028878050869736186900714720710555703168729087
    """

    # default prime (Mersenne prime Mp derived from p=521)
    p = (1 << 521) - 1

    def set_p(self, prime):
        type(self).p = prime
        return self

    @property
    def max_size(self):
        return (self.p.bit_length() + 7) // 8

    def __repr__(self):
        return status(
            ("kind", "encryptor/decryptor (shamir-secret-sharing)"),
            ("prime", self.p),
            ("data", self),
        )

    def help(self):
        super().help()
        usage(self.set_p, self.unload)

    @io()
    @silent
    def encrypt(self, n, k, data=None):
        if n < 0 or k < 0 or k > n:
            raise ValueError(f"Invalid n and k used: n={n}, k={k}.")
        secret = self.decimal()
        if secret >= self.p:
            raise ValueError(
                f"Secret exceeds MAX-SIZE available: {self.max_size}-byte."
            )
        f = [secret] + [secrets.randbelow(self.p) for _ in range(1, k)]
        shares = [(i, evalpoly(f, i, self.p)) for i in range(1, n + 1)]
        return shares

    @io()
    @silent
    def decrypt(self, data=None):
        shares = self.unload()
        xs, ys = zip(*shares)
        return int_to_bytes(lagrange_interpol(self.p, 0, xs, ys))

    @silent
    def load(self, data, op=None):
        def ser(o):
            s = self.max_size
            l = f_(self.lifter, op=op)
            return g_f(
                b"".join,
                m_(l),
                lambda xs: [
                    to_bytes(x, s) if i % 2 else to_bytes(x, 2)
                    for i, x in enumerate(xs)
                ],
                list,
                flatten,
            )(o)

        return super().load(data, ser=ser)

    @silent
    def unload(self, op="decimal"):
        s = self.max_size
        u = f_(self.dumper, op=op)
        o = tuple(range(0, self.length(), 2 + s))
        f = g_f(m_(bytes), f_(split_by, self))
        g = g_f(tuple, m_(g_f(u, bytes)), f_(flip(split_by), [2]))

        return [g(x) for x in f(o[1:])]
