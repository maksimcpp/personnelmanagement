import hashlib

def hash(token: str) -> str:
    algorithm = hashlib.sha256()
    algorithm.update(token.encode('utf-8'))
    hash_token = algorithm.hexdigest()
    return hash_token
