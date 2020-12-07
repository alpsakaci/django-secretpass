from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3", "type": "email"})
    )
    first_name = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control mb-3"})
    )
    last_name = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"class": "form-control mb-3"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class AccountForm(forms.ModelForm):
    service = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
    )
    repeat = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
    )

    class Meta:
        model = Account
        fields = ["service", "username", "password"]


class AccountUpdateForm(forms.Form):
    service = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control mb-3"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}), required=False
    )
    repeat = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={"class": "form-control mb-3"}),
        required=False,
    )
    use_current_password = forms.BooleanField(
        label="Use current password", required=False
    )
