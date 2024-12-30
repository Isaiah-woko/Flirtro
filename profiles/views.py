from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import LoginForm, EscortRegisterForm1, EscortRegisterForm2, EscortImageForm, ClientRegisterForm
from django.contrib.auth.decorators import login_required
import os
from .models import ClientProfile, Image, EscortProfile
from django.contrib.auth.models import User

# Check if the file uploaded is an image with an allowed extension
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Login view

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    # Handle POST request
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            # Check if user exists and authenticate
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in.")
                return redirect('/')
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Invalid form submission.")
    
    # Handle GET request
    else:
        form = LoginForm()

    return render(request, 'profiles/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')  # Adjust this to your main page URL

# Registration view
def signup_view(request):
    return render(request, 'profiles/signup.html')


def home_view(request):
    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EscortRegisterForm1, EscortRegisterForm2, EscortImageForm
from .models import EscortProfile, Image
from django.contrib.auth.models import User
from datetime import datetime

def escort_register1(request):
    if request.method == 'POST':
        form = EscortRegisterForm1(request.POST)
        if not form.is_valid():
            print("Form errors:", form.errors)
            return render(request, 'profiles/escort_register1.html', {'form': form})
        if form.is_valid():
            # Convert date_of_birth to string
            cleaned_data = form.cleaned_data
            cleaned_data['date_of_birth'] = cleaned_data['date_of_birth'].strftime('%Y-%m-%d')
            
            # Save data to the session
            request.session['step1_data'] = cleaned_data
            return redirect('profiles:escort_register2')
    else:
        form = EscortRegisterForm1()

    return render(request, 'profiles/escort_register1.html', {'form': form})

def escort_register2(request):
    step1_data = request.session.get('step1_data')  # Retrieve Step 1 data
    if not step1_data:
        return redirect('profiles:escort_register1')  # Redirect if step1 is incomplete

    if request.method == 'POST':
        form = EscortRegisterForm2(request.POST)
        if form.is_valid():
            step2_data = form.cleaned_data
            # Combine step1 and step2 data
            complete_data = {**step1_data, **step2_data}

            # Convert date_of_birth back to date object
            complete_data['date_of_birth'] = datetime.strptime(complete_data['date_of_birth'], '%Y-%m-%d').date()

            # Create a new User instance
            user = User.objects.create_user(username=complete_data['username'], email=complete_data['email'], password=complete_data['password'])

            # Save additional data in EscortProfile
            escort_profile = EscortProfile.objects.create(
                user=user,
                display_name=complete_data['display_name'],
                country=complete_data['country'],
                state=complete_data['state'],
                city=complete_data['city'],
                date_of_birth=complete_data['date_of_birth'],
                gender=complete_data['gender'],
                heading=complete_data['heading'],
                country_code=complete_data['country_code'],
                mobile_number=complete_data['mobile_number'],
                bust_size=complete_data['bust_size'],
                height=complete_data['height'],
                looks=complete_data['looks'],
                smoker=complete_data['smoker'],
                sexual_orientation=complete_data['sexual_orientation'],
                services=complete_data['services']
            )

            # Save the escort_profile id in the session for the next step
            request.session['escort_profile_id'] = escort_profile.id

            messages.success(request, "Step 2 completed successfully!")
            return redirect('profiles:escort_register3')
    else:
        form = EscortRegisterForm2()

    return render(request, 'profiles/escort_register2.html', {'form': form})


def escort_register3(request):
    escort_profile_id = request.session.get('escort_profile_id')
    if not escort_profile_id:
        return redirect('profiles:escort_register2')  # Redirect if step 2 is incomplete

    if request.method == 'POST':
        print(f"Request FILES: {request.FILES}")  # Log the request's FILES attribute
        form = EscortImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_images = form.cleaned_data['photo']
            escort_profile = EscortProfile.objects.get(id=escort_profile_id)
            for image in uploaded_images:
                Image.objects.create(escort_profile=escort_profile, photo=image)  # Save each uploaded image
            messages.success(request, "Your registration is complete!")
            return redirect('profiles:login')  # Redirect after successful upload
        else:
            print("Form errors:", form.errors)  # Debugging log

    else:
        form = EscortImageForm()

    return render(request, 'profiles/escort_register3.html', {'form': form})


# def register_complete(request):
#     return render(request, 'profiles/signup_complete.html')


def client_register(request):
    if request.method == 'POST':
        print("Form submitted!")
        form = ClientRegisterForm(request.POST, request.FILES)
        if not form.is_valid():
            print("Form errors:", form.errors)
            return render(request, 'profiles/client_register.html', {'form': form})
        if form.is_valid():
            print("Form is valid!")
            # Extract data from the form
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            display_name = form.cleaned_data['display_name']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            date_of_birth = form.cleaned_data['date_of_birth']
            gender = form.cleaned_data['gender']
            mobile_number = form.cleaned_data['mobile_number']
            profile_picture = form.cleaned_data.get('profile_picture')

            # Ensure password confirmation matches
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, 'profiles/client_register.html', {'form': form})

            # Create a new User instance
            user = User.objects.create_user(username=username, email=email, password=password)

            # Save additional data in ClientProfile
            ClientProfile.objects.create(
                user=user,
                display_name=display_name,
                country=country,
                state=state,
                city=city,
                date_of_birth=date_of_birth,
                gender=gender,
                mobile_number=mobile_number,
                profile_picture=profile_picture
            )

            messages.success(request, "Your account has been created successfully! Please log in.")
            return redirect('profiles:login')
    else:
        print("Form is invalid!")
        form = ClientRegisterForm()


    return render(request, 'profiles/client_register.html', {'form': form})

