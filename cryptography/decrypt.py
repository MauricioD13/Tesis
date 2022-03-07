from Crypto.Cipher import AES
import sys


def decrypt_msg(msg, key):
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce

    plaintext = cipher.decrypt(msg)


if __name__ == '__main__':

    decrypt_msg(sys.argv[1], sys.argv[2])
