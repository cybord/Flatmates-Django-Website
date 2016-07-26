from django import forms
from django.contrib.admin.widgets import AdminDateWidget

def today():
    from datetime import date
    return date.today().strftime("%d-%m-%Y")

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First name', max_length=100, )
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    joining_date = forms.DateField(widget=AdminDateWidget, help_text="DD-MM-YYYY",input_formats=['%d-%m-%Y'])
    company = forms.CharField(max_length=100)

class ExpenseForm(forms.Form):
    expense = forms.CharField(max_length=100)
    spent_amount = forms.IntegerField()
    description = forms.CharField(max_length=300)
