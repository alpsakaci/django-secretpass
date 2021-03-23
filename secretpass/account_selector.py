from django.db.models import Q
from django.contrib.auth.models import User
from secretpass.models import Account


def get_accounts_by_user(user):
    return Account.objects.filter(owner=user, is_deleted=False).order_by("date_created").reverse()


def get_account_by_id(id):
    return Account.objects.get(id=id)


def get_accounts_in_trash(user):
    return (Account.objects.filter(owner=user, is_deleted=True).order_by("date_created").reverse())


def search_accounts(user, query):
    query = Q(owner=user) & Q(is_deleted=False) & (
        Q(service__icontains=query) | Q(username__icontains=query))

    return Account.objects.filter(query)
