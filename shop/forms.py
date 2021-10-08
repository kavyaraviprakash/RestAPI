from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.widgets import DateInput
from .models import *
from django_countries.widgets import CountrySelectWidget



class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('address', 'city', 'state', 'zipcode', 'phone')


class CountryForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ('selectedcountry',)
        widgets = {'selectedcountry': CountrySelectWidget()}

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('Name', 'Comments_Or_Questions', 'Email', 'Phone_Number')