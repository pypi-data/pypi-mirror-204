import urllib3
from hasher import Keccak512


def check(password: str, test: bool = False) -> bool:
    hashed_password = Keccak512(password)
    https = urllib3.PoolManager()
    r = https.request("GET", f"https://passwords.xposedornot.com/api/v1/pass/anon/{hashed_password}")

    if r.data == b'{"Error":"Not found"}\n':
        if test:
            print("Is safe")
        return True
    else:
        return False
