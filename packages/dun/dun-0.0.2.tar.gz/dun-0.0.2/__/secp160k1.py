from __.curve import curve, ecdef
from __.utils import f_

secp160k1 = f_(
    curve,
    "secp160k1",
    ecdef(
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFAC73,
        a=0x0,
        b=0x7,
        gx=0x3B4C382CE37AA192A4019E763036F4F5DD4D7EBB,
        gy=0x938CF935318FDCED6BC28286531733C3F03C4FEE,
        n=0x0100000000000000000001B8FA16DFAB9ACA16B6B3,
        h=0x1,
    ),
)
