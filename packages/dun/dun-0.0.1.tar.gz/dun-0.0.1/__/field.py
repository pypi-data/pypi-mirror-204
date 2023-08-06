from itertools import zip_longest

from __.utils import (
    bytes_to_int,
    f_,
    fst,
    g_f_,
    int_to_bytes,
    random_znz,
    status,
    usage,
)


def egcd(a, b):
    """Extended Euclidean algorithm:
    If a = b * q + r, gcd(a, b) = gcd(b, r).
    Find (x,y) holding ax + by = gcd(a, b).
    """
    if b == 0:
        return 1, 0
    else:
        q = a // b
        r = a - q * b
        x, y = egcd(b, r)
        return y, x - q * y


def recip(x, p):
    return fst(egcd(x, p))


def nlzero(x):
    """normailize polynomials: remove leading zeros"""
    while x and x[-1] == 0:
        x.pop()
    return x


def deg(x):
    """degree of the given polynomial"""
    return len(nlzero(x)) - 1


@g_f_(nlzero)
def addpoly(f, g, p=None):
    """f(x) + g(x)  (mod p)"""
    if p:
        return [(x + y) % p for x, y in zip_longest(f, g, fillvalue=0)]
    else:
        return [x + y for x, y in zip_longest(f, g, fillvalue=0)]


@g_f_(nlzero)
def subpoly(f, g, p=None):
    """f(x) - g(x)  (mod p)"""
    if p:
        return [(x - y) % p for x, y in zip_longest(f, g, fillvalue=0)]
    else:
        return [x - y for x, y in zip_longest(f, g, fillvalue=0)]


@g_f_(nlzero)
def scalepoly(f, k, p=None):
    """f(x) * k  (mod p)"""
    if p:
        return [(k * x) % p for x in f]
    else:
        return [k * x for x in f]


@g_f_(nlzero)
def mulpoly(f, g, p=None):
    """f(x) * g(x)  (mod p)"""
    if not f:
        return []
    x, *xs = f
    return addpoly(scalepoly(g, x, p), ([0] + mulpoly(xs, g, p)), p)


@g_f_(nlzero)
def powpoly(f, k, p=None):
    """f(x) ** k  (mod p)"""
    if k < 0:
        raise ValueError(f"Negative exponent used: {k}")
    elif k == 0:
        return [1]
    elif k == 1:
        return scalepoly(f, 1, p)
    elif k % 2 == 0:
        g = powpoly(f, k // 2, p)
        return mulpoly(g, g, p)
    else:
        g = powpoly(f, k // 2, p)
        return mulpoly(f, mulpoly(g, g, p), p)


def divpoly(f, g, p=None):
    """f(x) / g(x)  (mod p)"""
    f, g = map(nlzero, [f[:], g[:]])
    df, dg = map(deg, [f, g])
    if dg < 0:
        raise ZeroDivisionError
    if dg == 0:
        if p:
            return scalepoly(f, recip(g[0], p), p), []
        else:
            return scalepoly(f, 1 / g[0], p), []
    if df >= dg:
        q = [0] * df
        while df >= dg:
            d = [0] * (df - dg) + g
            if p:
                k = (f[-1] * recip(d[-1], p)) % p
            else:
                k = f[-1] / float(d[-1])
            q[df - dg] = k
            d = scalepoly(d, k, p)
            f = subpoly(f, d, p)
            df = deg(f)
        r = f
    else:
        q = []
        r = scalepoly(f, 1, p)
    return nlzero(q), r


def evalpoly(f, x, p=None):
    """ "evaluate f(k) % p"""
    fx = 0
    for c in reversed(f):
        fx *= x
        fx += c
        if p:
            fx %= p
    return fx


def egcdpoly(f, g, p=None):
    """Extended Euclidean algorithm for polynomial:
    find (a,b) holding f(x)*a(x) + g(x)*b(x) = gcd(f(x),g(x))

    If p is None, the process is performed in the ring of polynomials
    with rational coefficients (Q). Otherwise, it works with the polynomials
    with integer coefficients modulo p, (Z/pZ).

    If p is a prime number, it works with the polynomials over GF(p)
    """
    if not g:
        return [1], []
    else:
        q, r = divpoly(f, g, p)
        a, b = egcdpoly(g, r, p)
        return b, subpoly(a, mulpoly(q, b, p), p)


class galois:
    """Base class for Galois Field or Finite Field, GF(q) or GF(p^k)

    F = Prime Field of characteristic p (base field)
    F[x] = polynomial f(x) of field F coefficient
    p(x) = irreducible monic polynomial of F[x] over F
    Quotient ring, F[x] / p(x) -> Extension Field!
    +----+--------------------------------------------------------------------+
    | p  | characteristic of field                                            |
    +----+--------------------------------------------------------------------+
    | k  | degree of field (Prime Field if k=1, Extension Field when k>1)     |
    +----+--------------------------------------------------------------------+
    | q  | degree of field (p ** q)                                           |
    +----+--------------------------------------------------------------------+
    | fX | polynomial f[X] over p in Extension-Field construction             |
    +----+--------------------------------------------------------------------+
    | pX | irreducible polynomial p(x) over p in Extension-Field construction |
    +----+--------------------------------------------------------------------+
    """

    __slots__ = "_char", "_deg", "_elem"

    def __new__(cls, char, deg):
        obj = super().__new__(cls)
        obj._char = char
        obj._deg = deg
        obj._elem = None
        return obj

    def __bool__(self):
        if self.e:
            return True
        else:
            return False

    def clone(self):
        return self.F(self.e)

    @property
    def _(self):
        self.help()

    def help(self):
        usage(self.help, self.clone, self.F, self.rand, header="galois")

    @property
    def p(self):
        """Characteristic of the Galois Field"""
        return self._char

    @property
    def k(self):
        """Degree of the Galois Field"""
        return self._deg

    @property
    def q(self):
        """Order of the Galois Field"""
        return self.p**self.k

    @property
    def e(self):
        """Element(field member) of this Galois Field"""
        return self._elem

    def F(self, o):
        """Field element constructor of the current field F"""
        raise NotImplementedError("Subclasses must implement this.")

    @property
    def zero(self):
        """Additive identity of this Galois Field"""
        raise NotImplementedError("Subclasses must implement this.")

    @property
    def one(self):
        """Multiplicative identity of this Galois Field"""
        raise NotImplementedError("Subclasses must implement this.")

    @property
    def recip(self):
        """Reciprocal of this Galois Field element"""
        raise NotImplementedError("Subclasses must implement this.")

    @property
    def rand(self):
        """Random element of this Galois Field"""
        raise NotImplementedError("Subclasses must implement this.")

    def neg(self):
        raise NotImplementedError("Subclasses must implement this.")

    def add(self, o):
        raise NotImplementedError("Subclasses must implement this.")

    def sub(self, o):
        raise NotImplementedError("Subclasses must implement this.")

    def mul(self, o):
        raise NotImplementedError("Subclasses must implement this.")

    def div(self, o):
        raise NotImplementedError("Subclasses must implement this.")

    def pow(self, o):
        raise NotImplementedError("Subclasses must implement this.")

    def __neg__(self):
        return self.neg()

    def __add__(self, o):
        return self.add(o)

    def __radd__(self, o):
        return self.__add__(o)

    def __sub__(self, o):
        return self.sub(o)

    def __rsub__(self, o):
        return self.__neg__().__add__(o)

    def __mul__(self, o):
        return self.mul(o)

    def __rmul__(self, o):
        return self.__mul__(o)

    def __truediv__(self, o):
        return self.div(o)

    def __rtruediv__(self, o):
        return o * self.recip

    def __pow__(self, o):
        return self.pow(o)


class pf(galois):
    """Representation of Prime Field"""

    __slots__ = ()

    def __new__(cls, char):
        obj = super().__new__(cls, char, 1)

        return f_(obj.load)

    def load(self, o=None):
        # set a field memeber of this Prime Field
        if o is None:
            return self.rand()
        elif isinstance(o, int):
            self._elem = o % self.p
        elif isinstance(o, bytes):
            self._elem = bytes_to_int(o) % self.p
        elif isinstance(o, str):
            self._elem = bytes_to_int(o.encode()) % self.p
        # read a field member from other object
        elif isinstance(o, pf):
            if self.p == o.p:
                self._elem = o.e
            else:
                raise ValueError(f"Different field used: {o}")
        else:
            raise ValueError(f"Not allowed field element: {o}")
        return self

    def F(self, o):
        return self.__class__(self.p)(o)

    @property
    def eb(self):
        """Byte representation of this Prime Field element"""
        size = (self.p.bit_length() + 7) // 8
        return int_to_bytes(self.e, size)

    @property
    def zero(self):
        return self.F(0)

    @property
    def one(self):
        return self.F(1)

    @property
    def recip(self):
        return self.F(recip(self.e, self.p))

    def rand(self):
        return self.F(random_znz(self.p))

    def __repr__(self):
        if self.e is None:
            return f"F({self.p})"
        else:
            return status(("field", f"F({self.p})"), ("elem", f"'{self.e}"))

    def __str__(self):
        return f"'{self.e}"

    def __int__(self):
        return self.e

    def __eq__(self, o):
        if not isinstance(o, pf):
            return False
        return self.p == o.p and self.e == o.e

    def neg(self):
        return self.F(-self.e)

    def add(self, o):
        return self.F(self.e + self.F(o).e)

    def sub(self, o):
        return self.F(self.e - self.F(o).e)

    def mul(self, o):
        if isinstance(o, int) or isinstance(o, pf):
            return self.F(self.e * self.F(o).e)
        else:
            return self.e * o

    def div(self, o):
        return self * self.F(o).recip

    def pow(self, o):
        exp = int(o) % (self.p - 1)
        return self.F(pow(self.e, exp, self.p))


class ef(galois):
    """Representation of Extension Field"""

    __slots__ = "_ip"

    def __new__(cls, char, ip):
        obj = super().__new__(cls, char, len(ip) - 1)

        # set an irreducible polynomial of this Extension Field
        obj._ip = scalepoly(ip, 1, obj.p)
        return f_(obj.load)

    def load(self, o=None):
        if o is None:
            return self.rand()
        # set a field memeber of this Extension Field
        elif isinstance(o, list):
            _, self._elem = divpoly(o, self.ip, self.p)
        # read a field member from other object
        elif isinstance(o, ef):
            if self.p == o.p and self.ip == o.ip:
                self._elem = o.e
            else:
                raise ValueError(f"Different field used: {o}")
        else:
            raise ValueError(f"Not allowed extension field element: {o}")
        return self

    def F(self, o):
        return self.__class__(self.p, self.ip)(o)

    @property
    def ip(self):
        """Irreducible Polynomial of this Extension Field"""
        return self._ip

    @property
    def zero(self):
        return self.F([0])

    @property
    def one(self):
        return self.F([1])

    @property
    def recip(self):
        (x, y) = egcdpoly(self.e, self.ip, self.p)
        k = addpoly(mulpoly(self.e, x), mulpoly(self.ip, y))
        return self.F(scalepoly(x, recip(k[0], self.p), self.p))

    def rand(self):
        return self.F([random_znz(self.p) for _ in range(self.k + 1)])

    def __repr__(self):
        if self.e is None:
            return f"EF({self.p}, {self.ip})"
        else:
            return status(("field", f"EF({self.p}, {self.ip})"), ("elem", f"'{self.e}"))

    def __str__(self):
        return f"`{self.e}"

    def __eq__(self, o):
        if not isinstance(o, ef):
            return False
        return self.p == o.p and self.ip == o.ip and self.e == o.e

    def neg(self):
        return self.F(scalepoly(self.e, -1, self.p))

    def add(self, o):
        return self.F(addpoly(self.e, self.F(o).e, self.p))

    def sub(self, o):
        return self.F(subpoly(self.e, self.F(o).e, self.p))

    def mul(self, o):
        return self.F(mulpoly(self.e, self.F(o).e, self.p))

    def div(self, o):
        return self * self.F(o).recip

    def pow(self, k):
        if not isinstance(k, int):
            raise ValueError(f"Exponent is NOT an integer: {k}")
        if k < 0:
            raise ValueError(f"Negative exponent used: {k}")
        elif k == 0:
            return self.F([1])
        elif k == 1:
            return self
        elif k % 2 == 0:
            g = self.__pow__(k // 2)
            return g * g
        else:
            g = self.__pow__(k // 2)
            return self * (g * g)
