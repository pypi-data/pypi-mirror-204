from collections import namedtuple

from __.field import galois, pf
from __.utils import random_znz, singleton, status, usage

ecdef = namedtuple("ecdef", "p, a, b, gx, gy, n, h")


class curve:
    """Weierstrass elliptic curve over GF(p): y^2 = x^3 + a*x + b
    +---+------------------------------------------------------------+
    | p | Characteristic of curve                                    |
    +---+------------------------------------------------------------+
    | a | Coefficient a in the curve equation                        |
    +---+------------------------------------------------------------+
    | b | Coefficient b in the curve equation                        |
    +---+------------------------------------------------------------+
    | G | Affine (x, y) of G, base point of an elliptic curve group  |
    +---+------------------------------------------------------------+
    | n | Size of group of E(Fp), |E(Fp)|                            |
    +---+------------------------------------------------------------+
    | h | Cofactor = n / r, n=|E(Fp)|, r=size of subgroup of E(Fp)   |
    +---+------------------------------------------------------------+

    - Coversion Montgomery form into Weierstrass form
    Montgomery form:
        By^2 = x^3 + Ax^2 + x
    Weierstrass form:
        v^2 = t^3 + at + b

    point map: (x, y) -> (t, v) = (x/B + A/3B, y/B)
    a = (3 - A^2) / 3B^2
    b = (2A^3 - 9A) / 27B^3
    """

    __slots__ = "name", "_ecdef"

    def __new__(cls, name, ecdef, k=None, *args, **kwargs):
        obj = super().__new__(cls)
        obj.name = name
        obj._ecdef = ecdef
        if k is None:
            return obj
        else:
            if isinstance(k, bytes):
                k = k.decimal()
            return obj.kG(k)

    def __repr__(self):
        return status(
            ("kind", self.__str__()),
            ("p", self.p),
            ("a", self.a),
            ("b", self.b),
            ("G.x", self.gx),
            ("G.y", self.gy),
            ("n", self.n),
            ("h", self.h),
        )

    def __str__(self):
        return f"elliptic curve ({self.name})"

    def __eq__(self, o):
        if isinstance(o, curve):
            return all(
                [getattr(self, k) == getattr(o, k) for k in ecdef.__dict__["_fields"]]
            )
        else:
            return False

    @property
    def _(self):
        self.help()

    def help(self):
        usage(self.help, self.kG, self.randp, self.ap, self.jp, header=self.name)

    @property
    def p(self):
        return self._ecdef.p

    @property
    def a(self):
        return self._ecdef.a

    @property
    def b(self):
        return self._ecdef.b

    @property
    def gx(self):
        return self._ecdef.gx

    @property
    def gy(self):
        return self._ecdef.gy

    @property
    def n(self):
        return self._ecdef.n

    @property
    def h(self):
        return self._ecdef.h

    @property
    def bits(self):
        return self.p.bit_length()

    @property
    def bytes(self):
        return (self.bits + 7) // 8

    @property
    def G(self):
        return A(self, self.gx, self.gy)

    def kG(self, k=None):
        if k is None:
            return self.randp()
        return self.G.mul(k)

    def randp(self):
        return self.G.mul(random_znz(self.p))

    def ap(self, x, y):
        """Affine point on this curve"""
        return A(self, x, y)

    def jp(self, X, Y, Z):
        """Jocobian point on this curve"""
        return J(self, X, Y, Z)


class point:
    """Points on elliptic curve, E
    +----+---------------------------------------------------------------------+
    | ap | Constructor representing Affine point, (x,y)                        |
    +----+---------------------------------------------------------------------+
    | jp | Constructor representing Jacobian point, (X,Y,Z) = (X/Z^2,Y/Z^3,Z)  |
    +----+---------------------------------------------------------------------+
    | O  | Point at Infinity                                                   |
    +----+---------------------------------------------------------------------+
    O in Jacobian coordinates: (X,Y,Z) = (t^2,t^3,0) = (1,1,0) when t = 1

    EQ-test for Jacobian point:

        J1(X1 Y1 Z1) ==? J2(X2 Y2 Z2)
        X1 * Z2 ^ 2 == X2 * Z1 ^ 2 && Y1 * Z2 ^ 3 == Y2 * Z1 ^ 3
    """

    __slots__ = ()

    def __neg__(self):
        return self.inv()

    def __add__(self, o):
        return self.add(o)

    def __radd__(self, o):
        return self.add(o)

    def __sub__(self, o):
        return self.sub(o)

    def __rsub__(self, o):
        return self.inv().add(o)

    def __mul__(self, k):
        return self.mul(k)

    def __rmul__(self, k):
        return self.mul(k)

    @property
    def _(self):
        self.help()

    def help(self):
        usage(
            self.help,
            self.on_curve,
            self.at_infinity,
            self.inv,
            self.dbl,
            self.add,
            self.sub,
            self.mul,
            self.toA,
            self.toJ,
            self.to_bytes,
            header="point",
        )

    def on_curve(self):
        """Check if this point is on the curve"""
        raise NotImplementedError("Subclasses must implement this.")

    def at_infinity(self):
        """Check if this point is at infinity"""
        raise NotImplementedError("Subclasses must implement this.")

    def inv(self):
        """Flip point on x-axis"""
        raise NotImplementedError("Subclasses must implement this.")

    def dbl(self):
        """Point doubling"""
        raise NotImplementedError("Subclasses must implement this.")

    def add(self, p):
        """Point addition"""
        raise NotImplementedError("Subclasses must implement this.")

    def sub(self, p):
        """Point substraction"""
        raise NotImplementedError("Subclasses must implement this.")

    def mul(self, k):
        """Point scalar multiplication"""
        raise NotImplementedError("Subclasses must implement this.")

    def toA(self):
        """Affine point to Jacobian point"""
        raise NotImplementedError("Subclasses must implement this.")

    def toJ(self):
        """Jacobian point to Affine point"""
        raise NotImplementedError("Subclasses must implement this.")

    def to_bytes(self, compressed=None):
        """Convert the point on curve into bytes representation"""
        raise NotImplementedError("Subclasses must implement this.")


@singleton
class O(point):
    """Point at Infinity"""

    __slots__ = ()

    def __repr__(self):
        return "O (point at infinity)"

    def __eq__(self, o):
        return isinstance(o, type(self))

    def toA(self):
        return self

    def toJ(self):
        return self

    def to_bytes(self, compressed=None):
        raise ValueError("Point at Infinity can't convert into bytes")

    def on_curve(self):
        return True

    def at_infinity(self):
        return True

    def inv(self):
        return self

    def dbl(self):
        return self

    def add(self, p):
        return p

    def sub(self, p):
        return p.inv()

    def mul(self, k):
        return self


O = O()


def _0_from_curve(curve):
    """Guess the field additive identity from curve parameters"""
    if isinstance(curve.a, galois):
        return curve.a.zero
    else:
        return pf(curve.p)(0)


def _1_from_curve(curve):
    """Guess the field multiplication identity from curve parameters"""
    if isinstance(curve.a, galois):
        return curve.a.one
    else:
        return pf(curve.p)(1)


class A(point):
    """Elliptic curve point in Affine coordinate"""

    __slots__ = "_on", "_x", "_y"

    def __new__(cls, curve, x, y):
        obj = super().__new__(cls)
        obj._on = curve
        o = _0_from_curve(obj.on)
        obj._x = o + x
        obj._y = o + y
        return obj

    @property
    def on(self):
        return self._on

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        return status(
            ("curve", f"Affine point (on {self.on.name})"), ("x", self.x), ("y", self.y)
        )

    def __eq__(self, o):
        o = isinstance(o, A) and o or o.toA()
        return all([getattr(self, k) == getattr(o, k) for k in self.__slots__])

    def toA(self):
        return self

    def toJ(self):
        return J(self.on, self.x, self.y, self.x.one)

    def to_bytes(self, compressed=False):
        if compressed:
            parity = self.y.e % 2 == 0 and b"\x02" or b"\x03"
            return parity + self.x.eb
        else:
            return self.x.eb + self.y.eb

    def on_curve(self):
        return self.y**2 == (self.x**2 + self.on.a) * self.x + self.on.b

    def at_infinity(self):
        return False

    def inv(self):
        if self.at_infinity():
            return self
        else:
            return self.__class__(self.on, self.x, -self.y)

    def dbl(self):
        e = _1_from_curve(self.on)
        e2 = e + e
        e3 = e2 + e
        l = (e3 * self.x**2 + self.on.a) / (e2 * self.y)
        x = l**2 - self.x - self.x
        y = l * (self.x - x) - self.y
        return self.__class__(self.on, x, y)

    def add(self, p):
        if p.at_infinity():
            return self
        if self == p:
            return self.dbl()
        elif self.inv() == p:
            return O
        else:
            p = isinstance(p, A) and p or p.toA()
            l = (self.y - p.y) / (self.x - p.x)
            x = l * l - self.x - p.x
            y = l * (self.x - x) - self.y
            return self.__class__(self.on, x, y)

    def sub(self, p):
        p = isinstance(p, A) and p or p.toA()
        return self.add(p.inv())

    def mul(self, k):
        if isinstance(k, point):
            raise ValueError("Not allowed (*) between points")
        if isinstance(k, galois):
            k = k.e
        if k < 0:
            return self.mul(abs(k)).inv()
        elif k == 0:
            return O
        elif k == 1:
            return self
        elif k % 2 == 0:
            return self.dbl().mul(k // 2)
        else:
            return self.dbl().mul(k // 2).add(self)


class J(point):
    """Elliptic curve point in Jacobian coordinate"""

    __slots__ = "_on", "_X", "_Y", "_Z"

    def __new__(cls, curve, X, Y, Z):
        obj = super().__new__(cls)
        obj._on = curve
        o = _0_from_curve(obj.on)
        obj._X = o + X
        obj._Y = o + Y
        obj._Z = o + Z
        if obj.at_infinity():
            return O
        else:
            return obj

    @property
    def on(self):
        return self._on

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Z(self):
        return self._Z

    def __repr__(self):
        return status(
            ("curve", f"Jacobian point (on {self.on.name})"),
            ("X", self.X),
            ("Y", self.Y),
            ("Z", self.Z),
        )

    def __eq__(self, o):
        return self.toA() == o.toA()

    def toA(self):
        if not self.Z:
            return O
        else:
            return A(self.on, self.X / self.Z**2, self.Y / self.Z**3)

    def toJ(self):
        return self

    def to_bytes(self, compressed=False):
        return self.toA().to_bytes(compressed)

    def on_curve(self):
        return self.Y**2 == (self.X**2 + self.on.a * self.Z**4) * self.X + (
            self.on.b * self.Z**6
        )

    def at_infinity(self):
        if (not self.Z) and (self.X**3 == self.Y**2):
            return True
        else:
            return False

    def inv(self):
        return self.toA().inv().toJ()

    def dbl(self):
        return self.toA().dbl().toJ()

    def add(self, p):
        return self.toA().add(p).toJ()

    def sub(self, p):
        return self.toA().sub(p).toJ()

    def mul(self, k):
        return self.toA().mul(k).toJ()
