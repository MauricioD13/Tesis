from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import binascii
import os


def load_key():

    with open('./mosq-ca.key', 'r') as src:
        privKey = RSA.import_key(src.read())
    pubKey = privKey.publickey()

    with open('./mosq-ca.pub', 'wb') as src_w:
        src_w.write(pubKey.export_key())
    return privKey, pubKey


def msg_signature(msg, keyPair, pubKey):

    msg = msg.encode('utf-8')
    print(msg)
    hash = SHA256.new(msg)
    signer = PKCS115_SigScheme(keyPair)
    signature = signer.sign(hash)
    print("Signature:", binascii.hexlify(signature))
    return signature


def verify_sign(msg, keyPair, pubKey, signature):

    msg = msg.encode('utf-8')
    hash = SHA256.new(msg)
    verifier = PKCS115_SigScheme(pubKey)
    try:
        verifier.verify(hash, signature)
        print("Signature is valid.")
    except:
        print("Signature is invalid.")


def encrypt_msg(key, msg):

    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(msg)
    return ciphertext, tag


if __name__ == '__main__':
    privKey, pubKey = load_key()
    msg = 'Mensaje de prueba'
    signature = msg_signature(msg, privKey, pubKey)
    verify_sign(msg, privKey, pubKey, signature)
    msg = msg + binascii.hexlify(signature).decode('utf-8')

    crypt_msg, tag = encrypt_msg(b'clave_secreta_13', msg.encode('utf-8'))
    # Tipo: Bytes -> crypt_msg
    crypt_msg = binascii.hexlify(crypt_msg).decode('utf-8')
    os.system(f'mosquitto_pub -t /prueba -d -h 192.168.1.10 -m "{crypt_msg}"')
