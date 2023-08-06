import hashlib

# import pytest
from __ import *


def t(label, a, b):
    print(f"{label:>16}  {b}")
    assert a == b, label


def test_hashers():
    key = b"kakaobank"
    print()
    t(
        "blake2b",
        __("blake2b").load(key).hash().hex(),
        hashlib.blake2b(key).hexdigest(),
    )
    t(
        "blake2s",
        __("blake2s").load(key).hash().hex(),
        hashlib.blake2s(key).hexdigest(),
    )
