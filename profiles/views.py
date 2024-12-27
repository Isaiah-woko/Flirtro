from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .forms import LoginForm, EscortRegisterForm1, EscortRegisterForm2, ClientRegisterForm
# from .models import User
from django.contrib.auth.decorators import login_required
import os
from .models import ClientProfile
from django.contrib.auth.models import User

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
                if hasattr(user, 'clientprofile'):
                    return redirect('dashboard:client_dashboard')
                # elif hasattr(user, 'profile2'):
                #     # Custom behavior for profile2
                #     return redirect('profile2_dashboard')
                messages.success(request, "You have been logged in.")
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, "Invalid form submission.")
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


FORMS = [
    ("step1", EscortRegisterForm1),
    ("step2", EscortRegisterForm2),  # Ensure RegisterForm2 is passed as a class
]



class MultiStepFormWizard(SessionWizardView):
    # Define the forms and their steps
    form_list = FORMS

    def get_template_names(self):
        """
        Override this method to render different templates for each step.
        """
        step = self.steps.current  # Get the current step
        
        if step == 'step1':
            return ['profiles/escort_register1.html']  # Template for Step 1
        elif step == 'step2':
            return ['profiles/escort_register2.html']  # Template for Step 2
        # Add more steps as needed
        return ['profiles/signup.html']  # Fallback template

    def done(self, form_list, **kwargs):
        """
        This function is called when the form is completed (after the last step).
        """
        # Collect all form data
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        # Optionally save to the database or send an email
        # Example: Save the data to a model here

        # Flash a success message
        messages.success(self.request, "Your form has been successfully submitted!")

        # Redirect to a "thank you" or completion page
        return HttpResponseRedirect('/form/complete')


def form_complete(request):
    # Render a template or send a response indicating the form submission is complete
    return render(request, 'profiles/form_complete.html')



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

