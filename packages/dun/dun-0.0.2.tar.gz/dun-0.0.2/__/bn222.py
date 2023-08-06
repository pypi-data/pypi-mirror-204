from __.curve import curve, ecdef
from __.utils import f_

bn222 = f_(
    curve,
    "BN-222",
    ecdef(
        p=0x23DC0D7DC02402CDE486F4C00015B5215C0000004C6CE00000000067,
        a=0x0,
        b=0x101,
        gx=0x23DC0D7DC02402CDE486F4C00015B5215C0000004C6CE00000000066,
        gy=0x10,
        n=0x23DC0D7DC02402CDE486F4C00015555156000000496DA00000000061,
        h=0x1,
    ),
)
