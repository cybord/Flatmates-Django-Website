from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First name', max_length=100, )
    last_name = forms.CharField(label='Last name', max_length=100)
