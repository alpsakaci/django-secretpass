from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from secretpass.models import Account
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
import json
from django.views import generic
from secretpass.forms import (
    AccountForm,
    AccountUpdateForm,
    UserRegisterForm,
    MasterKeyRegisterForm,
    SetMasterKeyForm,
)
from .views import AccountViewSet
from .serializers import AccountSerializer
from .settings import SP_PASSPHRASE
from secretpass.decorators import keychecker_required, masterkey_required
import base64
from secretpass.account_selector import get_accounts_by_user, get_account_by_id, get_accounts_in_trash, search_accounts
from secretpass.account_service import create_account, update_account, decrypt_account_password, move_to_trash, restore as restore_from_trash
from secretpass.encryption_service import decrypt_password


@login_required(login_url="/secretpass/login")
@keychecker_required
@masterkey_required
def index(request):
    accounts = get_accounts_by_user(request.user)
    context = {"accounts": accounts}

    return render(request, "secretpass/index.html", context)


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("spindex")
    template_name = "secretpass/signup.html"


@login_required(login_url="/secretpass/login")
@keychecker_required
@masterkey_required
def create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            service = form.cleaned_data["service"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            repeat = form.cleaned_data["repeat"]

            if password.__eq__(repeat):
                master_password= decrypt_password(request.session.get("user_masterkey"), bytes(SP_PASSPHRASE, 'utf-8'))
                create_account(request.user, service, username, password, master_password)
            else:
                context = {"form": form}
                form.add_error("password", "Password does not match.")
                return render(request, "secretpass/create.html", context)

            return redirect(index)
    else:
        form = AccountForm()
        context = {"form": form}

    return render(request, "secretpass/create.html", context)


@login_required(login_url="/secretpass/login")
@keychecker_required
@masterkey_required
def edit(request, acc_id):
    if request.method == "POST":
        form = AccountUpdateForm(request.POST)

        if form.is_valid():
            service = form.cleaned_data["service"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            repeat = form.cleaned_data["repeat"]
            use_current_password = form.cleaned_data["use_current_password"]

            acc = get_object_or_404(
                Account.objects.filter(id=acc_id, owner=request.user)
            )
            if use_current_password == True:
                acc.service = service
                acc.username = username
                acc.save()
            elif password != "" and password.__eq__(repeat):
                master_password= decrypt_password(request.session.get("user_masterkey"), bytes(SP_PASSPHRASE, 'utf-8'))
                update_account(acc, service, username, password, master_password)
            else:
                context = {"form": form, "account_id": acc.id}
                form.add_error("password", "Password does not match.")
                return render(request, "secretpass/edit.html", context)

            return redirect(index)
    else:
        account = get_object_or_404(
            Account.objects.filter(id=acc_id, owner=request.user)
        )
        form = AccountUpdateForm(
            initial={"service": account.service, "username": account.username}
        )
        context = {"form": form, "account": account}

    return render(request, "secretpass/edit.html", context)


@login_required(login_url="/secretpass/login")
@keychecker_required
@masterkey_required
def decrypt(request, acc_id):

    if request.method == "POST":
        account = Account.objects.get(owner=request.user, id=acc_id)
        master_password= decrypt_password(request.session.get("user_masterkey"), bytes(SP_PASSPHRASE, 'utf-8'))
        
        load = {
            "plain_password": decrypt_account_password(account, master_password)
        }
        data = json.dumps(load)

        return HttpResponse(data, content_type="application/json")


@login_required(login_url="/secretpass/login")
def movetotrash(request, acc_id):
    if request.method == "POST":
        account = get_object_or_404(
            Account.objects.filter(id=acc_id, owner=request.user)
        )
        move_to_trash(account)

    return redirect(index)


@login_required(login_url="/secretpass/login")
def restore(request, acc_id):
    if request.method == "POST":
        account = get_object_or_404(
            Account.objects.filter(id=acc_id, owner=request.user)
        )
        restore_from_trash(account)

    return redirect(index)


@login_required(login_url="/secretpass/login")
def delete(request, acc_id):
    if request.method == "POST":
        account = get_object_or_404(
            Account.objects.filter(id=acc_id, owner=request.user)
        )
        account.delete()

    return redirect(index)


@login_required(login_url="/secretpass/login")
def trash(request):
    accounts = get_accounts_in_trash(request.user)
    context = {"accounts": accounts}

    return render(request, "secretpass/index.html", context)
