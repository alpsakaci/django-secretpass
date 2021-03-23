from functools import wraps
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from .forms import SetMasterKeyForm, MasterKeyRegisterForm
from .settings import SP_PASSPHRASE
import base64
from secretpass.profile_service import create_profile, check_master_password
from secretpass.encryption_service import encrypt_password


def keychecker_required(view_func):
    @wraps(view_func)
    def check(request, *args, **kwargs):
        try:
            request.user.profile
            return view_func(request, *args, **kwargs)
        except Exception:
            if request.method == "POST":
                form = MasterKeyRegisterForm(request.POST)
                if form.is_valid():
                    masterkey1 = form.cleaned_data["masterkey1"]
                    masterkey2 = form.cleaned_data["masterkey2"]

                    if masterkey1.__eq__(masterkey2):
                        create_profile(request.user, masterkey1)

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
                    
                    try:
                        check_master_password(masterkey, request.user.profile.salt, request.user.profile.master_password)
                        request.session["user_masterkey"] = encrypt_password(masterkey, bytes(SP_PASSPHRASE, 'utf-8'))
                        
                        return view_func(request, *args, **kwargs)
                    except:
                        form.add_error("masterkey", "Key is not valid.")
            context = {"form": form}

            return render(request, "secretpass/set_masterkey.html", context)
        else:
            return view_func(request, *args, **kwargs)

    return check
