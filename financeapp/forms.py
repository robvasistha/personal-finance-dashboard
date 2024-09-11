from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Custom user creation form for registration
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  # This automatically hashes the password
        return user

# Custom authentication form for login
class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(
        label='Email or Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})  # No email validation here
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request  # Ensure the request is stored
        self.user_cache = None  # Cache the user after authentication
        super().__init__(*args, **kwargs)  # Pass args and kwargs to the parent class

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            # Authenticate using the request, username, and password
            self.user_cache = authenticate(request=self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid login details.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
