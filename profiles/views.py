from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .forms import LoginForm, RegisterForm
from .models import User, Role
import os

# Check if the file uploaded is an image with an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in.")
                return redirect('main:index')  # Adjust this to your main page URL
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'profiles/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('main:index')  # Adjust this to your main page URL

# Registration view
def signup_view(request):
    return render(request, 'profiles/signup.html')


def home_view(request):
    return render(request, 'home.html')


# Escort Registration view
def escort_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role_id = form.cleaned_data['role']
            specialty = form.cleaned_data['specialty']
            bio = form.cleaned_data['bio']
            image = form.cleaned_data['image']

            # Create new user and set password
            user = User.objects.create_user(username=username, password=password)

            # Assign the role to the user
            role = Role.objects.get(id=role_id)
            user.roles.add(role)

            # Add other fields like specialty and bio
            user.specialty = specialty
            user.bio = bio

            # Save profile image if uploaded
            if image and allowed_file(image.name):
                filename = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
                with open(filename, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                user.image_filename = image.name

            user.save()
            messages.success(request, "Your user has been created, please login.")
            return redirect('profiles:login')
    else:
        form = RegisterForm()
    return render(request, 'profiles/escort_register.html', {'form': form})

# Client Registration view
def client_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role_id = form.cleaned_data['role']
            specialty = form.cleaned_data['specialty']
            bio = form.cleaned_data['bio']
            image = form.cleaned_data['image']

            # Create new user and set password
            user = User.objects.create_user(username=username, password=password)

            # Assign the role to the user
            role = Role.objects.get(id=role_id)
            user.roles.add(role)

            # Add other fields like specialty and bio
            user.specialty = specialty
            user.bio = bio

            # Save profile image if uploaded
            if image and allowed_file(image.name):
                filename = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
                with open(filename, 'wb') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                user.image_filename = image.name

            user.save()
            messages.success(request, "Your user has been created, please login.")
            return redirect('profiles:login')
    else:
        form = RegisterForm()
    return render(request, 'profiles/client_register.html', {'form': form})


# Fetch countries for registration (AJAX)
def get_countries(request):
    form = RegisterForm()
    countries = form.populate_countries()
    return JsonResponse(countries, safe=False)


# Fetch states based on selected country (AJAX)
def get_states(request, country_geoname_id):
    form = RegisterForm()
    states = form.populate_states(country_geoname_id)
    return JsonResponse(states, safe=False)


# Fetch cities based on selected state (AJAX)
def get_cities(request, state_geoname_id):
    form = RegisterForm()
    cities = form.populate_cities(state_geoname_id)
    return JsonResponse(cities, safe=False)
