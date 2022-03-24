from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from cryptography.fernet import Fernet
import binascii
import os
import time



def cipher_v2(mensaje):
    cipher_key = b'miwgjlluTr_7g0NPVM9TsUKyr8ri_Q6FKirxniums0U='

    cipher = Fernet(cipher_key)

    #Encriptar
    encrypted_message = cipher.encrypt(mensaje)
    print(encrypted_message)
    out_message = encrypted_message.decode()
    print(out_message)

    return out_message


def load_key():

    with open('./mosq-ca.key', 'r') as src:
        privKey = RSA.import_key(src.read())
    pubKey = privKey.publickey()

    with open('./mosq-ca.pub', 'wb') as src_w:
        src_w.write(pubKey.export_key())
    return privKey, pubKey


def msg_signature(msg, keyPair, pubKey):

    #msg = msg.encode('utf-8')
    print(msg)
    hash = SHA256.new(msg)
    signer = PKCS115_SigScheme(keyPair)
    signature = signer.sign(hash)
    print("Signature:", signature)
    return signature


def verify_sign(msg, pubKey, signature):

    #msg = msg.encode('utf-8')
    hash = SHA256.new(msg)
    print(hash)
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
    msg = b'Si sirve'
    separador = b' - '
    signature = msg_signature(msg, privKey, pubKey)
    verify_sign(msg, pubKey, signature)
    print(type(msg))
    print(type(signature))
     
    msg = msg + separador + signature

    
    #AES

    #print(type(msg))
    #msg = msg.encode('utf-8') 
    #print(type(msg))

    #crypt_msg, tag = encrypt_msg(b'clave_secreta_13', msg)
    #print(crypt_msg)
    #crypt_msg = binascii.hexlify(crypt_msg)
    #print(crypt_msg)
    #print(dir(crypt_msg))
    #crypt_msg = crypt_msg.decode('utf-8')
    crypt_msg = cipher_v2(msg)

    os.system(f'mosquitto_pub -t /prueba -d -h 192.168.1.10 -m "{crypt_msg}"')
