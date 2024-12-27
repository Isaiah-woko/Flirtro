from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import Role
import pycountry
import requests
from .models import ClientProfile
from django.core.files.storage import FileSystemStorage

# Allowed extensions for the image
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    remember = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            self.add_error(None, "Both username and password are required.")
            raise ValidationError("Both username and password are required.")

        # Search for the ClientProfile and check the user's password
        try:
            client_profile = ClientProfile.objects.get(user__username=username)
            if not client_profile.user.check_password(password):
                self.add_error(None, "Invalid username or password.")
                raise ValidationError("Invalid username or password")
        except ClientProfile.DoesNotExist:
            self.add_error(None, "Invalid username or password.")
            raise ValidationError("Invalid username or password")
        
        return cleaned_data

# Registration Form
class EscortRegisterForm1(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    display_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Female', 'Female'), ('Male', 'Male')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    heading = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_code = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Optional image field
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        # Check if username already exists
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("User with that name already exists")

        return cleaned_data
    

class ClientRegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    display_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.ChoiceField(choices=[('Nigeria', 'Nigeria')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Female', 'Female'), ('Male', 'Male')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        # Check if username already exists
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"The username '{username}' is already taken. Please choose a different one.")


        return cleaned_data



class EscortRegisterForm2(forms.Form):
    bust_size = forms.ChoiceField(choices=[('', 'Choose Option'),
                                           ('Enormous(E+)', 'Enormous(E+)'),
                                           ('Large(C-Cup)', 'Large(C-Cup)'),
                                           ('Large(D-Cup)', 'Large(D-Cup)'),
                                           ('Medium(B-Cup)', 'Medium(B-Cup)'),
                                           ('Small(A)', 'Small(A)'),
                                           ('Very Large(DD-Cup)', 'Very Large(DD-Cup)'),
                                           ('Very Small', 'Very Small'),
                                           ('None', 'None')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    height = forms.ChoiceField(choices=[('Average', 'Average'),
                                        ('Large(C-Cup)', 'Large(C-Cup)'),
                                        ('Not Too Tall', 'Not Too Tall'),
                                        ('Portable', 'Portable'),
                                        ('Tall', 'Tall'),
                                        ('Very Tall', 'Very Tall')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    looks = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    smoker = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')], 
                               required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    sexual_orientation = forms.ChoiceField(choices=[('Bisexual', 'Bisexual'),
                                           ('Heterosexual', 'Heterosexual'),
                                           ('Lesbian', 'Lesbian'),
                                           ('Gay', 'Gay'),
                                           ('Transsexual', 'Transsexual'),
                                           ('None', 'None')], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    services = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))