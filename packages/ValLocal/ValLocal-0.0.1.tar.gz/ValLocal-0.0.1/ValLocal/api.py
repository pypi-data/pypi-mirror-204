from typing import Dict, Literal
from requests import request, Response

from .parsing import encode
from .structs import LockFile


def auth(lock: LockFile) -> Dict[str, str]:
    token = encode(f"riot:{lock.password}")
    return {
        "Authorization": f"Basic {token}"
    }


def req(lock: LockFile, uri: str):
    base = f"127.0.0.1:{lock.port}"
    return f"https://{base}{uri}"


Methods = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]


def local_api(lock: LockFile, method: Methods, path: str, *, params=None, json=None) -> Response:
    headers = auth(lock)
    url = req(lock, path)
    return request(method, url, headers=headers, verify=False, params=params, json=json)
