class pipe:
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs

    def __ror__(self, o):
        try:
            f = o.__getattribute__(self.f)
            return f(*self.args, **self.kwargs)
        except Exception as e:
            print(f"\nerror: {e}\n")
            return o.__new__(o.__class__)

    def __call__(self, *args, **kwargs):
        return pipe(self.f.__name__, *args, **kwargs)


@pipe
def doc(*args, **kwargs):
    pass


@pipe
def help(*args, **kwargs):
    pass


@pipe
def length(*args, **kwargs):
    pass


@pipe
def rand(*args, **kwargs):
    pass


@pipe
def hash(*args, **kwargs):
    pass


@pipe
def encode(*args, **kwargs):
    pass


@pipe
def decode(*args, **kwargs):
    pass


@pipe
def encrypt(*args, **kwargs):
    pass


@pipe
def decrypt(*args, **kwargs):
    pass


@pipe
def sign(*args, **kwargs):
    pass


@pipe
def verify(*args, **kwargs):
    pass


@pipe
def setup(*args, **kwargs):
    pass


@pipe
def prove(*args, **kwargs):
    pass


@pipe
def load(*args, **kwargs):
    pass


@pipe
def unload(*args, **kwargs):
    pass


@pipe
def dump(*args, **kwargs):
    pass


@pipe
def loadf(*args, **kwargs):
    pass


@pipe
def dumpf(*args, **kwargs):
    pass


@pipe
def utf8(*args, **kwargs):
    pass


@pipe
def decimal(*args, **kwargs):
    pass


@pipe
def hex(*args, **kwargs):
    pass


@pipe
def base16(*args, **kwargs):
    pass


@pipe
def base32(*args, **kwargs):
    pass


@pipe
def base58(*args, **kwargs):
    pass


@pipe
def base64(*args, **kwargs):
    pass


@pipe
def base85(*args, **kwargs):
    pass


@pipe
def ascii85(*args, **kwargs):
    pass


@pipe
def set_p(*args, **kwargs):
    pass


@pipe
def set_curve(*args, **kwargs):
    pass


@pipe
def set_hasher(*args, **kwargs):
    pass
