from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import AccountForm, AccountUpdateForm, UserRegisterForm
from .views import AccountViewSet
from .serializers import AccountSerializer
from .crypto import encrypt_password, decrypt_password


@login_required(login_url="/secretpass/login")
def index(request):
    accounts = Account.get_user_accounts(request.user)
    context = {"accounts": accounts}

    return render(request, "secretpass/index.html", context)


class SignUpView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy("spindex")
    template_name = "secretpass/signup.html"


@login_required(login_url="/secretpass/login")
def create(request):
    if request.method == "POST":
        form = AccountForm(request.POST)

        if form.is_valid():
            service = form.cleaned_data["service"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            repeat = form.cleaned_data["repeat"]

            if password.__eq__(repeat):
                Account.create(
                    owner=request.user,
                    service=service,
                    username=username,
                    password=password,
                )
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
                acc.service = service
                acc.username = username
                acc.password = encrypt_password(password)
                acc.save()
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
def movetotrash(request, acc_id):
    if request.method == "POST":
        Account.move_to_trash(acc_id, request.user)

    return redirect(index)


@login_required(login_url="/secretpass/login")
def restore(request, acc_id):
    if request.method == "POST":
        Account.restore(acc_id, request.user)

    return redirect(index)


@login_required(login_url="/secretpass/login")
def delete(request, acc_id):
    if request.method == "POST":
        account = get_object_or_404(Account.objects.filter(id=acc_id, owner=request.user))
        account.delete()

    return redirect(index)


@login_required(login_url="/secretpass/login")
def trash(request):
    trash_items = Account.get_trash_items(request.user)
    context = {"accounts": trash_items}

    return render(request, "secretpass/index.html", context)
