from django import forms
from mycrypt.validators import NumberValidator, SymbolValidator, UppercaseValidator
from mycrypt.models import *
# will use after finish basic website


class UserForm(forms.Form):
    userAccount = forms.CharField(
        required=True,
        widget=forms.EmailField

    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        validators=[NumberValidator, UppercaseValidator, SymbolValidator],
    )
