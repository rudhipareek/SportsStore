from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomLoginForm(LoginForm):
    
    def clean(self):
        # First check if the user exists
        username = self.cleaned_data.get('login', '')
        if username:
            # Check if this username or email exists
            user_exists = User.objects.filter(username=username).exists() or \
                         User.objects.filter(email=username).exists()
            
            if not user_exists:
                # User doesn't exist - show the "no account exists" message
                raise forms.ValidationError(
                    "No account exists with this username. Please create an account."
                )
        
        # If we get here, try to authenticate normally
        try:
            return super().clean()
        except forms.ValidationError as e:
            # For all other errors, including wrong password, show this message
            raise forms.ValidationError(
                "Invalid credentials. Check username and password and try again."
            )

class CustomSignupForm(SignupForm):
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email address is already registered. Please use a different email or log in to your existing account."
            )
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "This username is already taken. Please choose a different username."
            )
        return username