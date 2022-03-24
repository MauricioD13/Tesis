import requests
import json
from credentials import identity_hash
import importlib.util
from config import AUTH_param, CONFIDENTIALITY, INTEGRITY


def http_post(crypt_msg):
    print(type(crypt_msg))
    msg = 'Mensaje de prueba'
    data = {'msg': crypt_msg}
    hash_id = identity_hash('1')
    data['id'] = '1'
    data['hash'] = hash_id
    resp = requests.post('http://127.0.0.1:5000/post', data=json.dumps(data))
    print(resp.content)


def get():
    requests.get('http://127.0.0.1:5000/get', headers={'host': 'example.com'})


if __name__ == '__main__':
    spec = importlib.util.spec_from_file_location(
        "rsa", "/home/guasonito/Documents/Universidad/Tesis/Tesis/cryptography/rsa.py")
    rsa = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rsa)

    message = 'Si sirve'

    if CONFIDENTIALITY == 1 and INTEGRITY == 1:
        crypt_msg = rsa.cipher_signature(message)
    elif INTEGRITY == 1:
        crypt_msg = rsa.just_signature(message)
    else:
        crypt_msg = message
    http_post(crypt_msg)
