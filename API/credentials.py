from hashlib import sha256


def identity_hash(id):
    h = sha256()
    secret = 'ClaveSecreta'
    h.update(bytes(id+secret, 'utf-8'))
    return h.hexdigest()
