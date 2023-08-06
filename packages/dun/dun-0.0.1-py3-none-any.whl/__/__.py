import sys
from collections import namedtuple
from importlib import import_module

from __.utils import group_by

impl = namedtuple("impl", "hasher, encoder, encryptor, signer, curve, custom")

modules = impl(
    # hashers
    [
        "blake2b",
        "blake2s",
        "hash160",
        "keccak256",
        "md4",
        "md5",
        "md5_sha1",
        "mdc2",
        "pbkdf2_hmac",
        "ripemd160",
        "sha1",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "sha224",
        "sha256",
        "sha384",
        "sha512",
        "sha512_224",
        "sha512_256",
        "shake_128",
        "shake_256",
        "sm3",
        "whirlpool",
    ],
    # encoders
    ["ascii85", "base16", "base32", "base58", "base64", "base85"],
    # encryptors
    [
        "aes_cbc",
        "aes_cfb",
        "aes_ctr",
        "aes_ecb",
        "aes_ofb",
        "elgamal",
        "paillier",
        "rsa",
        "sss",
    ],
    # signers
    ["ecdsa", "eddsa", "elgamal-dsa", "schnorr"],
    # elliptic curves
    [
        "bls12-381",
        "bls12-446",
        "bls12-455",
        "bls12-638",
        "bls24-477",
        "bn128",
        "bn128-2",
        "bn128-12",
        "bn158",
        "bn190",
        "bn222",
        "bn254",
        "bn286",
        "bn318",
        "bn350",
        "bn382",
        "bn414",
        "bn446",
        "bn478",
        "bn510",
        "bn542",
        "bn574",
        "bn606",
        "bn638",
        "p-192",
        "p-224",
        "p-256",
        "p-384",
        "p-521",
        "secp160k1",
        "secp160r1",
        "secp160r2",
        "secp192k1",
        "secp192r1",
        "secp224k1",
        "secp224r1",
        "secp256k1",
        "secp256r1",
        "secp384r1",
        "secp521r1",
    ],
    # custom modules
    ["keys"],
)


def load_modules():
    """Imort all implemented modules"""
    for k in modules._asdict().keys():
        for e in getattr(modules, k):
            import_module(f"__.{to_fname(e)}")


def list_modules():
    for k in modules._asdict().keys():
        print()
        print(k)
        for l in group_by(getattr(modules, k), 4, ""):
            print("{:>18}{:>18}{:>18}{:>18}".format(*l))
        print()


def to_fname(s):
    """Convert case-insensitive selector names into valid filenames"""
    return s.replace("-", "_").lower()


def __(opName=None, *args, **kwargs):
    """Operation selector:
    +-----------+-----------------------------------------+
    | hasher    | hash algorithm                          |
    |-----------+-----------------------------------------|
    | encoder   | encode/decode algorithm                 |
    |-----------+-----------------------------------------|
    | encryptor | encrypt/decrypt algorithm               |
    |-----------+-----------------------------------------|
    | signer    | digital signature algorithm (DSA)       |
    |-----------+-----------------------------------------|
    | curve     | elliptic curve over GF(q)               |
    |-----------+-----------------------------------------|
    | point     | affine/jacobian point on elliptic curve |
    +-----------+-----------------------------------------+
    """
    if opName is None:
        list_modules()
        return

    path = f"__.{to_fname(opName)}"
    try:
        op = getattr(sys.modules[path], to_fname(opName))
    except:
        op = None

    if op is not None:
        return op(*args, **kwargs)
    else:
        sys.exit(f"No such operation: {opName}")
