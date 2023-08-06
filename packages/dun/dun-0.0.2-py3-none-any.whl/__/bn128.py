from __.curve import curve, ecdef
from __.utils import f_

# BN (Barreto-Naehrig) curve 128-bit security
bn128 = f_(
    curve,
    "BN-128",
    ecdef(
        p=21888242871839275222246405745257275088696311157297823662689037894645226208583,
        a=0,
        b=3,
        gx=1,
        gy=2,
        n=21888242871839275222246405745257275088548364400416034343698204186575808495617,
        h=1,
    ),
)
