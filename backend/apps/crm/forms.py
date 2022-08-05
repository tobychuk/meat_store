from django import forms
from backend.apps.crm.models import Debt, Client

class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = [
            'debtor',
            'quantity',
            'amount_meat',
            'created',
            'return_date',

        ]
        widgets = {
            "quantity":forms.TextInput(attrs={"class": "form-control"}),
            "amount_meat":forms.TextInput(attrs={"class": "form-control"}),
            "created":forms.DateInput(attrs={"class":" form-control", "type": "date"}),
            "return_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'phone_number',
            'reserve_phone_number',
            'address',
            'passport_image_first',
            'passport_image_second'

        ]
        widgets = {
            "first_name":forms.TextInput(attrs={"class": "form-control"}),
            "last_name":forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "reserve_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))