from secretpass.models import Profile
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from rest_framework.exceptions import ParseError


def create_profile(user, master_password):
    profile = Profile(user=user)
    profile.salt = generate_salt(encode=True)
    profile.master_password = hash_master_password(master_password, profile.salt)
    profile.full_clean()
    profile.save()

    return profile


def generate_salt(encode=False):
    salt = get_random_bytes(16)
    if encode == True:
        return b64encode(salt).decode("utf-8")
    else:
        return salt


def hash_master_password(master_password, salt):
    hasher = SHA512.new()
    hasher.update(bytes(master_password + salt, encoding="utf-8"))

    return hasher.hexdigest()


def check_master_password(master_password, salt, hash):
    if hash_master_password(master_password, salt).__eq__(hash):
        return True
    else:
        raise ParseError("Master Password is not valid.")


def generate_key(master_password, salt):
    return PBKDF2(master_password, salt, 16, count=1000000, hmac_hash_module=SHA512)
