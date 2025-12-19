import hashlib


def gen_hash_512(data):
    return hashlib.sha512(data.encode("utf-8")).hexdigest()