from django.db.models import Q
from django.contrib.auth.models import User


def get_users():
    return User.objects.all()


def get_user_by_id(id):
    return User.objects.get(id=id)
