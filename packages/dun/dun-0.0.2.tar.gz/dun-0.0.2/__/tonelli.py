# Tonell-Shanks algorithm
# https://en.wikipedia.org/wiki/Tonelli–Shanks_algorithm


def eulerCriterion(a, p):
    """Euler's criterion (or Legendre symbol)
    (a | p) =  1 (mod p) if a is quadratic residue (a = x^2 && a /= 0) (mod p)
            = -1 (mod p) if a is non-quadratic residue
            =  0 (mod p) if a = 0 (mod p)
    """
    return pow(a, (p - 1) // 2, p)


def aRp(a, p):
    """predicate for Quadratic Residue
    'aRp' is the notation Gauss used for quadratic residues"""
    return eulerCriterion(a, p) == 1


def aNp(a, p):
    """predicate for Quadratic Residue
    'aNp' is the notation Gauss used for non-quadratic residues"""
    return eulerCriterion(a, p) == (p - 1)


def factorQ2S(p):
    """Find Q and S such that p-1 = Q * 2^S (with odd Q) by factoring out power of 2"""

    def go(q, s):
        if q & 1:
            return q, s
        else:
            return go(q >> 1, s + 1)

    return go(p - 1, 0)


def findz(p):
    """find any number 'z' has no square root (non-qaudratic residue) in [1,p)"""
    return next((z for z in range(1, p) if aNp(z, p)), None)


def sqrt_zpz(n, p):
    """Find sqrt(n) over Z/pZ based on Tonelli-Shanks
    'p' is a odd prime (p is a prime and p /= 2)

    Algorithm:
    1. Factorize (p-1) out power of two:  p-1 = Q * 2^S
    2. Search for a non-quadratic residue, z in Z/pZ
    3. Set M <- S, c <- z^Q, t <- n^Q, R <- n^((Q+1)/2)
    4. Loop: (as shown below)
      - if t=0, return 0
      - if t=1, return R
      - otherwise, find the least i such that t^(2^i) = 1 for [1, M)
        b = c^(2^(M-i-1))
      - set the below and repeat
        M <- i, c <- b^2, t <- t*b^2, R <- R*b
    """

    def loop(M, c, t, R):
        if t == 0:
            return 0
        elif t == 1:
            return R
        else:
            i = next((i for i in range(1, M) if pow(t, (2**i), p) == 1), None)
            if i is None:
                raise ValueError("Can't find i satisfying t^(2^i)=1: t={t}")
            b = pow(c, pow(2, (M - i - 1), p), p)
            return loop(i, (b * b) % p, (t * b * b) % p, (R * b) % p)

    if aNp(n, p):
        return
    else:
        Q, S = factorQ2S(p)
        z = findz(p)
        if z:
            M = S
            c = pow(z, Q, p)
            t = pow(n, Q, p)
            R = pow(n, ((Q + 1) // 2), p)
            return loop(M, c, t, R)
        else:
            raise RuntimeError(f"Broken Tonelli-Shank's algorithm: r^2={n} (mod {p})")
