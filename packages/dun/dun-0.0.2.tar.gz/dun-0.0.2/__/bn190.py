from __.curve import curve, ecdef
from __.utils import f_

bn190 = f_(
    curve,
    "BN-190",
    ecdef(
        p=0x240001B0000948001E60004134005F10005DC0003A800013,
        a=0x0,
        b=0x1001,
        gx=0x240001B0000948001E60004134005F10005DC0003A800012,
        gy=0x40,
        n=0x240001B0000948001E600040D4005CD0005760003180000D,
        h=0x1,
    ),
)
