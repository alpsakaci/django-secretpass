from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from rest_framework.exceptions import ParseError

def encrypt_password(password, key):
    data = bytes(password, encoding="utf-8")
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = b64encode(cipher.nonce).decode("utf-8")
    tag = b64encode(tag).decode("utf-8")
    ciphertext = b64encode(ciphertext).decode("utf-8")

    return nonce + tag + ciphertext


def decrypt_password(password, key):
    try:
        nonce = b64decode(password[:24])
        tag = b64decode(password[24:48])
        ciphertext = b64decode(password[48:])
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext.decode("utf-8")
    except:
        raise ParseError('Key is not valid')
