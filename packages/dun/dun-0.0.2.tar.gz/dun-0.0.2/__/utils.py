import os
from datetime import datetime, timedelta
from functools import partial, reduce, wraps
from inspect import signature
from itertools import islice, zip_longest
from operator import itemgetter
from textwrap import fill


def id(x):
    return x


def fst(x):
    return itemgetter(0)(x)


def snd(x):
    return itemgetter(1)(x)


def flip(f):
    """flip(f) takes its arguments in the reverse order of f"""

    @wraps(f)
    def wrapper(*args):
        return f(*args[::-1])

    return wrapper


def g_f(*fs):
    """function composition using the given list of functions"""

    def wrapper(f, g):
        return lambda x: f(g(x))

    return reduce(wrapper, fs, id)


def g_f_(*fs):
    """Decorator of function composition using the given list of functions.
    The result of wrapped function will be evaluated again by the decorator
    of function composition
    """

    def comp(g):
        @wraps(g)
        def wrapper(*args, **kwargs):
            return g_f(*fs)(g(*args, *kwargs))

        return wrapper

    return comp


# partial evaluation of function
f_ = partial


def m_(f):
    """Builds partially applied map
    map(f, xs) == f <$> xs

    (f <$>) == map(f, )  == f_(map, f) == m_(f)
    (<$> xs) == map( ,xs) == f_(flip(map), xs)
    """
    return f_(map, f)


def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def bytes_to_int(x, byteorder="big"):
    return int.from_bytes(x, byteorder=byteorder)


def int_to_bytes(x, size=None, byteorder="big"):
    if size is None:
        size = (x.bit_length() + 7) // 8
    return x.to_bytes(size, byteorder=byteorder)


def random_bytes(n):
    return os.urandom(n)


def random_znz(n):
    """Random integers modulo a given n, Z/nZ"""
    return bytes_to_int(random_bytes((n.bit_length() + 7) // 8)) % n


def flatten(xss):
    if isinstance(xss, tuple) or isinstance(xss, list):
        for xs in xss:
            yield from flatten(xs)
    else:
        yield xss


def split_by(o, i):
    """Split list/tuple by the given splitting-indices"""
    i = [0] + list(i) + [None]
    return tuple(islice(o, begin, end) for begin, end in zip(i, i[1:]))


def group_by(o, size, fill=None):
    """Group list/tuple by the given group size"""
    return list(zip_longest(*(iter(o),) * size, fillvalue=fill))


def status(*records):
    return "\n".join(
        fill(
            f"{v}",
            width=95,
            break_on_hyphens=False,
            drop_whitespace=False,
            initial_indent=f"{k:>8}" + "  |  ",
            subsequent_indent="          |  ",
        )
        for k, v in records
    )


def usage(*fs, header=None):
    if header:
        print(f"{header}:")
    print("\n".join(f"    {f.__name__}{signature(f)}" for f in fs))


def pad(x):
    """Pad data using PKCS7 (16-byte)
    EM = M || PS, where PS = 16-(||M|| mod 16)
    """
    return x + (16 - len(x) % 16) * chr(16 - len(x) % 16).encode()


def unpad(x):
    """Unpad data for AES-decoding (see also pad() function):
    These pad/unpad functions keeps cipher blocks from padding attack
    """
    return x[: -ord(x[-1:].decode())]


def timestamp(origin=None, w=0, d=0, h=0, m=0, s=0, from_fmt=None, to_fmt=False):
    if from_fmt:
        t = datetime.strptime(from_fmt, "%Y-%m-%dT%H:%M:%S.%f%z").timestamp()
    else:
        dt = timedelta(weeks=w, days=d, hours=h, minutes=m, seconds=s).total_seconds()
        if origin is None:
            origin = datetime.utcnow().timestamp()
        t = origin + dt

    return to_fmt and f"{datetime.fromtimestamp(t).isoformat()[:26]}Z" or t
