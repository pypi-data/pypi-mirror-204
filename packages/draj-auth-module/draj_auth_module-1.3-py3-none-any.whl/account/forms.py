from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login
from django.db.models import Q

from .models import UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",
                               validators=[validate_password], widget=forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'placeholder': 'Password'
            })
                               )
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg form-control-solid',
            'placeholder': 'Confirm Password'
        })
                                       )

    class Meta:
        fields = ["username", "email", "first_name", "last_name"]
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field_name

    def clean(self):
        cleaned_data = super().clean()
        confirm_password = cleaned_data.get("confirm_password")
        password = cleaned_data.get("password")
        if confirm_password != password:
            raise ValidationError({'password': "Password and confirm password does not matched."})


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field_name

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            if not UserProfile.objects.filter(Q(email=username) | Q(username=username)).exists():
                raise ValidationError("User does not exist with this username")
            userprofile_obj = UserProfile.objects.get(Q(email=username) | Q(username=username))
            if not userprofile_obj.user.check_password(password):
                raise ValidationError("Invalid password for this username.")
            if not userprofile_obj.user.is_active:
                raise ValidationError("User is not active.")
            self.user = userprofile_obj.user
            login(self.request, userprofile_obj.user)
        return self.cleaned_data
