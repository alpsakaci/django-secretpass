from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import secretpass.settings as settings


def generate_salt(encode=False):
    salt = get_random_bytes(16)
    if encode == True:
        return b64encode(salt).decode("utf-8")
    else:
        return salt


def hash_masterkey(masterkey, salt):
    hasher = SHA512.new()
    hasher.update(bytes(masterkey + salt, encoding="utf-8"))

    return hasher.hexdigest()


def check_masterkey(masterkey, salt, hash):
    if hash_masterkey(masterkey, salt).__eq__(hash):
        return True
    else:
        return False


def generate_key(masterkey, salt):
    return PBKDF2(masterkey, salt, 16, count=1000000, hmac_hash_module=SHA512)


def encrypt_password(password, masterkey):
    data = bytes(password, encoding="utf-8")
    cipher = AES.new(masterkey, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = b64encode(cipher.nonce).decode("utf-8")
    tag = b64encode(tag).decode("utf-8")
    ciphertext = b64encode(ciphertext).decode("utf-8")

    return nonce + tag + ciphertext


def decrypt_password(password, masterkey):
    try:
        nonce = b64decode(password[:24])
        tag = b64decode(password[24:48])
        ciphertext = b64decode(password[48:])
        cipher = AES.new(masterkey, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        return plaintext.decode("utf-8")
    except:
        return None #TODO: return exception
