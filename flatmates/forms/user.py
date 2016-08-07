from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from flatmates.utils import OptionalChoiceField
from django.core.validators import RegexValidator
alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only Characters are allowed')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,validators=[alpha])
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }
    username = forms.CharField(label='Username', max_length=100,validators=[alpha])
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First name', max_length=100, )
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    joining_date = forms.DateField(widget=AdminDateWidget, help_text="DD-MM-YYYY",input_formats=['%d-%m-%Y'])
    company = forms.CharField(max_length=100)

class ExpenseForm(forms.Form):

    expense = OptionalChoiceField(choices=(("","_ _ _ _ _ _ _"),("Groceries","Groceries"),("Electricity Bill","Electricity Bill"), ("Net Bill","Net Bill"), ("Cable BIll","Cable BIll"),("Water Bill","Water Bill")))
    spent_amount = forms.IntegerField()
    description = forms.CharField(required=False)

class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput())
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
