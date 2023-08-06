import base64


def encode(string: str):
    bString = string.encode("utf-8")
    b64Str = base64.b64encode(bString)
    return b64Str.decode("utf-8")


def decode(string: str):
    bString = string.encode("utf-8")
    b64Str = base64.urlsafe_b64decode(bString)
    return b64Str.decode("utf-8")
