from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Role
import pycountry
import requests
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

        if username and password:
            user = User.objects.filter(username=username).first()
            if not user:
                raise ValidationError("Invalid username or password")
            if not user.check_password(password):
                raise ValidationError("Invalid password")
        return cleaned_data


# Registration Form
class RegisterForm(forms.Form):
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
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm')

        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Check if username already exists
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("User with that name already exists")

        return cleaned_data

    def populate_countries(self):
        """Populate countries using GeoNames API."""
        response = requests.get(
            "http://api.geonames.org/countryInfoJSON",
            params={"username": "demo"}  # You can replace this with your GeoNames username
        )
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json().get('geonames', [])
        return [(country["countryCode"], country["countryName"]) for country in data]

    def populate_states(self, country_geoname_id):
        """Populate states dynamically using GeoNames API."""
        response = requests.get(
            "http://api.geonames.org/childrenJSON",
            params={"geonameId": country_geoname_id, "username": "demo"}  # Replace with your username
        )
        data = response.json().get('geonames', [])
        return [(state["geonameId"], state["name"]) for state in data]

    def populate_cities(self, state_geoname_id):
        """Populate cities dynamically based on the selected state."""
        response = requests.get(
            "http://api.geonames.org/childrenJSON",
            params={"geonameId": state_geoname_id, "username": "demo"}  # Replace with your username
        )
        data = response.json().get('geonames', [])
        return [(city["geonameId"], city["name"]) for city in data]
