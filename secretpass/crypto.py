from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import secretpass.settings as settings


def encrypt_password(password):
    data = bytes(password, encoding="utf-8")
    key = bytes(settings.SP_PASSPHRASE, encoding="utf-8")
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = b64encode(cipher.nonce).decode("utf-8")
    tag = b64encode(tag).decode("utf-8")
    ciphertext = b64encode(ciphertext).decode("utf-8")

    return nonce + tag + ciphertext


def decrypt_password(password):
    try:
        key = bytes(settings.SP_PASSPHRASE, encoding="utf-8")
        nonce = b64decode(password[:24])
        tag = b64decode(password[24:48])
        ciphertext = b64decode(password[48:])
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext
    except:
        return None
