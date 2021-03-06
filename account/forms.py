from django import forms
from django.contrib.auth import get_user_model
from .utils import send_activation_email

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'last_name', 'group', 'phone', 'password', 'password_confirmation')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with given email already exists')
        return email
    
    def clean_group(self):
        group = self.cleaned_data.get("group")
        if group == 'admin':
            raise forms.ValidationError('you can\'t register as admin')
        return group

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.pop('password_confirmation')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        send_activation_email(email=user.email, activation_code=user.activation_code)
        return user

