from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class BuyerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'buyer'
        if commit:
            user.save()
        return user

class SellerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'seller'
        user.is_approved = False  # Seller must be approved by admin
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_blocked:
            raise forms.ValidationError('This account is blocked.', code='blocked')
        if user.role == 'seller' and not user.is_approved:
            raise forms.ValidationError('Seller account is not approved yet.', code='not_approved')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'address') 