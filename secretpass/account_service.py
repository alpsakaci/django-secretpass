from secretpass.models import Account
from secretpass.encryption_service import encrypt_password, decrypt_password
from secretpass.profile_service import check_master_password, generate_key


def create_account(owner, service, username, password, master_password):
    check_master_password(master_password, owner.profile.salt, owner.profile.master_password)
    account = Account(owner=owner, service=service, username=username)
    key = generate_key(master_password, owner.profile.salt)
    account.password = encrypt_password(password, key)
    account.full_clean()
    account.save()

    return account

def update_account(account, service, username, password, master_password):
    check_master_password(master_password, account.owner.profile.salt, account.owner.profile.master_password)
    account.service = service
    account.username = username
    key = generate_key(master_password, account.owner.profile.salt)
    account.password = encrypt_password(password, key)
    account.full_clean()
    account.save()

    return account

def decrypt_account_password(account, master_password):
    key = generate_key(master_password, account.owner.profile.salt)
    plain_password = decrypt_password(account.password, key)

    return plain_password

def move_to_trash(account):
    account.is_deleted = True
    account.save()


def restore(account):
    account.is_deleted = False
    account.save()

def delete_account(account):
    account.delete()
