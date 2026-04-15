from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomerRegistrationForm(UserCreationForm):
    """Form for customer registration"""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model  = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role  = 'customer'        # ← force role to customer
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class VendorRegistrationForm(UserCreationForm):
    """Form for vendor registration"""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model  = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role  = 'vendor'          # ← force role to vendor
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Simple login form"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)