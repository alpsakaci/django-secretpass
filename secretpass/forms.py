from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Account


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
