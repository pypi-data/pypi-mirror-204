from __.curve import curve, ecdef
from __.utils import f_

bn158 = f_(
    curve,
    "BN-158",
    ecdef(
        p=0x24240D8241D5445106C8442084001384E0000013,
        a=0x0,
        b=0x11,
        gx=0x24240D8241D5445106C8442084001384E0000012,
        gy=0x4,
        n=0x24240D8241D5445106C7E3F07E0010842000000D,
        h=0x1,
    ),
)
