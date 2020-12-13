from functools import wraps
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import KeyChecker
from .forms import SetMasterKeyForm, MasterKeyRegisterForm
from .crypto import generate_key, check_masterkey, generate_salt, hash_masterkey
import base64


def keychecker_required(view_func):
    @wraps(view_func)
    def check(request, *args, **kwargs):
        try:
            keychecker = KeyChecker.objects.get(owner=request.user)
            return view_func(request, *args, **kwargs)
        except ObjectDoesNotExist:
            if request.method == "POST":
                form = MasterKeyRegisterForm(request.POST)
                if form.is_valid():
                    masterkey1 = form.cleaned_data["masterkey1"]
                    masterkey2 = form.cleaned_data["masterkey2"]

                    if masterkey1.__eq__(masterkey2):
                        checker = KeyChecker(owner=request.user)
                        checker.salt = generate_salt(encode=True)
                        checker.keyhash = hash_masterkey(masterkey1, checker.salt)
                        checker.save()

                        return view_func(request, *args, **kwargs)
                    else:
                        context = {"form": form}
                        form.add_error("masterkey1", "Masterkeys do not match.")
                        return render(request, "secretpass/masterkey.html", context)

            form = MasterKeyRegisterForm()
            context = {"form": form}
            return render(request, "secretpass/masterkey.html", context)

    return check


def masterkey_required(view_func):
    @wraps(view_func)
    def check(request, *args, **kwargs):
        if request.session.get("user_masterkey") is None:
            form = SetMasterKeyForm()
            if request.method == "POST":
                form = SetMasterKeyForm(request.POST)
                if form.is_valid():
                    masterkey = form.cleaned_data["masterkey"]
                    keychecker = KeyChecker.objects.get(owner=request.user)

                    if check_masterkey(masterkey, keychecker.salt, keychecker.keyhash):
                        request.session["user_masterkey"] = masterkey
                        
                        return view_func(request, *args, **kwargs)
                    else:
                        form.add_error("masterkey", "Key is not valid.")
            context = {"form": form}

            return render(request, "secretpass/set_masterkey.html", context)
        else:
            return view_func(request, *args, **kwargs)

    return check
