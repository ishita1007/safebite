from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CustomUserCreationForm(UserCreationForm):
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget)

    class Meta:
        model = User
        fields = ('first_name','last_name', 'email','country','username', 'password1' )
