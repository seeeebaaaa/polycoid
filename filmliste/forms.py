from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_file_size

# test user
# User, 12345678@a

class SignupForm(UserCreationForm):
    type = forms.CharField(widget=forms.HiddenInput,initial="signup")
    email = forms.EmailField(required=True)  # Adding email field

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')  # Including email

class LoginForm(forms.Form):
    type = forms.CharField(widget=forms.HiddenInput,initial="login")
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfilePictureForm(forms.ModelForm):
    profile_picture = forms.ImageField(validators=[validate_file_size])
    class Meta:
        model = get_user_model()
        fields = ['profile_picture']