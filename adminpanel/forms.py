from django import forms
from .models import AdminLogin



class AdminLoginForm(forms.ModelForm):

    class Meta:
        model = AdminLogin
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'})

        }

        labels = {
            'email': 'email',
            'password': 'password',
        }