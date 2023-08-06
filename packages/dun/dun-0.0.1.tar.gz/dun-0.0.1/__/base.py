from functools import wraps

from __.__ import __
from __.utils import bytes_to_int, id, int_to_bytes, random_bytes, status, usage


def silent(f):
    """Keep calm and stay silent for things that are not important"""

    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            print(f"\nerror: {e}\n")
            return self.__new__(self.__class__, b"")

    return wrapper


def io(ok=id, data="data", lift=1):
    """Wraps input/output of Byteable methods"""

    def io_wrap(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            if data in kwargs:
                self = self.load(kwargs.get(data))
            if ok(self):
                r = f(self, *args, **kwargs)
                if lift:
                    return self.load(r)
                else:
                    return r
            else:
                return self

        return wrapper

    return io_wrap


def to_bytes(x, size=None):
    """Serialize available object into sequences of bytes (marshaling)"""
    if isinstance(x, bytes):
        return x
    elif isinstance(x, str):
        return x.encode()
    elif isinstance(x, int):
        return int_to_bytes(x, size)
    elif x is None:
        return b""
    else:
        raise ValueError(f"can't convert into bytes sequences, {x}")


def nilbyte_p(x):
    """check if the given argument is true or null-bytes-like"""
    return x or x == "" or x == b""


class Byteable(bytes):
    """Base class for byte-able object the following:
    +-----------+-----------+
    | kind      | method    |
    |-----------+-----------|
    | hasher    | hash()    |
    |-----------+-----------|
    | encoder   | encode()  |
    |           | decode()  |
    |-----------+-----------|
    | encryptor | encrypt() |
    |           | decrypt() |
    |-----------+-----------|
    | signer    | sign()    |
    |           | verify()  |
    +-----------+-----------+
    Don't forget to decorate those methods in child class with @io() and @silent.
    All implementations of bytes sequences follows 'big-endians'.
    """

    __slots__ = ()

    def __new__(cls, data=None):
        return super().__new__(cls, to_bytes(data))

    def __ror__(self, o):
        return self.load(o)

    def __(self, opName, *args, **kwargs):
        return __(opName, self, *args, **kwargs)

    @property
    def _(self):
        self.help()

    def help(self):
        usage(
            self.__,
            self.doc,
            self.help,
            self.length,
            self.rand,
            self.load,
            self.dump,
            self.loadf,
            self.dumpf,
            self.utf8,
            self.decimal,
            self.base16,
            self.base32,
            self.base58,
            self.base64,
            self.base85,
            self.ascii85,
            header="byteable",
        )

    def doc(self):
        return help(self)

    def length(self):
        return len(self)

    def rand(self, size=1 << 4):
        return self.load(random_bytes(size))

    @silent
    def load(self, data, ser=to_bytes, **kwargs):
        """Lift data onto Byteable using 'ser' (marshalling/serialization)"""
        return self.__new__(self.__class__, ser(data), **kwargs)

    @silent
    def unload(self, *args, **kwargs):
        """Unmarshal/deserialize byteable object using 'der' function"""
        raise NotImplementedError(
            "Implement this if needed to unmarshal byteable object"
        )

    @silent
    def dump(self, op="base64", *args):
        if op == "hex":
            return self.hex()
        elif op == "decimal":
            return self.decimal()
        elif op in {
            "base16",
            "base32",
            "base58",
            "base64",
            "base85",
            "ascii85",
        }:
            return self.__(op).encode().utf8()
        else:
            raise ValueError(f"Invalid operation: {op}")

    @silent
    def loadf(self, filepath):
        with open(filepath, "rb") as f:
            return self.load(f.read())

    @silent
    def dumpf(self, op, filepath):
        with open(filepath, "wb") as f:
            f.write(self.dump(op).encode())
        return self

    @silent
    def utf8(self):
        return bytes.decode(self)

    @silent
    def decimal(self):
        return bytes_to_int(self)

    @silent
    def base16(self):
        return self.dump("base16")

    @silent
    def base32(self):
        return self.dump("base32")

    @silent
    def base58(self):
        return self.dump("base58")

    @silent
    def base64(self):
        return self.dump("base64")

    @silent
    def base85(self):
        return self.dump("base85")

    @silent
    def ascii85(self):
        return self.dump("ascii85")

    @silent
    def lifter(self, o, op=None):
        """Helper function for serialization"""
        if op is not None:
            return __(op).load(o).decode()
        else:
            return to_bytes(o)

    @silent
    def dumper(self, o, op=None):
        """Helper function for deserialization"""
        if op is not None:
            # return self.load(o).dump(op)
            return Byteable().load(o).dump(op)
        else:
            return o


class Hasher(Byteable):
    """Base class for hashers"""

    __slots__ = ()

    def __repr__(self):
        return status(("kind", f"hasher ({self.__class__.__name__})"), ("data", self))

    def help(self):
        super().help()
        usage(self.hash, header=f"{self.__class__.__name__}")

    @io(nilbyte_p)
    @silent
    def hash(self, *args, data=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")


class Encoder(Byteable):
    """Base class for encoder/decoder"""

    __slots__ = ()

    def __repr__(self):
        return status(
            ("kind", f"encoder/decoder ({self.__class__.__name__})"), ("data", self)
        )

    def help(self):
        super().help()
        usage(self.encode, self.decode, header=f"{self.__class__.__name__}")

    @io()
    @silent
    def encode(self, *args, data=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")

    @io()
    @silent
    def decode(self, *args, data=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")


class Encryptor(Byteable):
    """Base class for encryptor/decryptor"""

    __slots__ = ()

    def __repr__(self):
        return status(
            ("kind", f"encryptor/decryptor ({self.__class__.__name__})"), ("data", self)
        )

    def help(self):
        super().help()
        usage(self.encrypt, self.decrypt, header=f"{self.__class__.__name__}")

    @io()
    @silent
    def encrypt(self, *args, data=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")

    @io()
    @silent
    def decrypt(self, *args, data=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")


class Signer(Byteable):
    """Base class for signer/verifier
    +---------+--------------------------------------+
    | privkey | private key used when signing        |
    |---------+--------------------------------------|
    | pubkey  | public key used when verifying       |
    |---------+--------------------------------------|
    | message | plain(unhashed) message to be signed |
    |---------+--------------------------------------|
    | curve   | elliptic curve to be used in DSA     |
    |---------+--------------------------------------|
    | hasher  | hash function to be used in DSA      |
    +---------+--------------------------------------+
    Byteable 'self' differently plays a role each context:
    when sign():   self -> message
    when verify(): self -> signature
    """

    def __repr__(self):
        return status(
            ("kind", f"signer/verifier ({self.__class__.__name__})"),
            ("curve", self.curve),
            ("hasher", self.hasher.__class__.__name__),
            ("data", self),
        )

    def help(self):
        super().help()
        usage(
            self.set_curve,
            self.set_hasher,
            self.sign,
            self.verify,
            header=f"{self.__class__.__name__}",
        )

    @silent
    def load(self, data, ser=to_bytes, **kwargs):
        return (
            super()
            .load(data, ser=ser, **kwargs)
            .set_curve(self.curve)
            .set_hasher(self.hasher)
        )

    @property
    def curve(self):
        return getattr(self, "_curve", self.def_curve)

    @property
    def hasher(self):
        return getattr(self, "_hasher", self.def_hasher)

    def set_curve(self, curve=None):
        curve = curve or self.def_curve
        setattr(self, "_curve", curve)
        return self

    def set_hasher(self, hasher=None):
        hasher = hasher or self.def_hasher
        setattr(self, "_hasher", hasher)
        return self

    @property
    def def_curve(self):
        raise NotImplementedError("Subclasses must implement this.")

    @property
    def def_hasher(self):
        raise NotImplementedError("Subclasses must implement this.")

    @io(data="msg")
    @silent
    def sign(self, *args, msg=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")

    @io(data="sig", lift=0)
    @silent
    def verify(self, *args, sig=None, **kwargs):
        raise NotImplementedError("Subclasses must implement this.")
