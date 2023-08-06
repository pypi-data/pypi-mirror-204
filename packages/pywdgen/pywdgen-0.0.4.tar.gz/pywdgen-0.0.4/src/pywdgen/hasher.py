from Crypto.Hash import keccak


def Keccak512(password: str) -> str:
    k = keccak.new(digest_bits=512)
    k.update(str.encode(password))
    a = k.hexdigest()
    return a[0:10]



