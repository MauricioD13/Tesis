import time
import os
import binascii
import sys
from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


def load_key():
    with open('./mosq-ca.pub', 'r') as src:
        pubKey = RSA.import_key(src.read())

    return pubKey


def verify_sign(msg, pubKey, signature):

    hash = SHA256.new(msg)
    verifier = PKCS115_SigScheme(pubKey)

    try:
        verifier.verify(hash, signature)
        print("[Firma valida]")

    except:
        print("[Firma invalida]")


def decrypt_msg(crypt_message):
    # Llave de cifrado
    cipher_key = b'miwgjlluTr_7g0NPVM9TsUKyr8ri_Q6FKirxniums0U='
    cipher = Fernet(cipher_key)

    # Desencriptar

    bytes_message = crypt_message.encode()
    message_signa = cipher.decrypt(bytes_message)

    # Arreglar mensaje recibido
    str_message = str(message_signa)
    arr_message = str_message.split(' - ')
    message = arr_message[0]
    signa_rx = arr_message[1]
    message = message[2:]
    signa_rx = signa_rx.replace('"', '')

    # Comprobar firma

    message = message.encode()
    signa_rx2 = signa_rx.encode()
    signa_rx2 = signa_rx2.decode('unicode_escape').encode('ISO-8859-1')

    pubKey = load_key()
    verify_sign(message, pubKey, signa_rx2)

    return message


def integrity_confirm(message_signa):

    # Arreglar mensaje recibido
    str_message = str(message_signa)
    arr_message = str_message.split(' - ')
    message = arr_message[0]
    signa_rx = arr_message[1]
    message = message[2:]
    signa_rx = signa_rx.replace('"', '')

    # Comprobar firma

    message = message.encode()
    signa_rx2 = signa_rx.encode()
    signa_rx2 = signa_rx2.decode('unicode_escape').encode('ISO-8859-1')

    pubKey = load_key()
    verify_sign(message, pubKey, signa_rx2)

    return message


if __name__ == '__main__':
    print(decrypt_msg(sys.argv[1]))

