from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .forms import LoginForm, EscortRegisterForm1, EscortRegisterForm2, ClientRegisterForm
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
# Escort Registration view
# def escort_register(request):
#     if request.method == 'POST':
#         form = RegisterForm1(request.POST, request.FILES)
#         if form.is_valid():
#             # Temporarily save the form data in the session
#             request.session['username'] = form.cleaned_data['username']
#             request.session['email'] = form.cleaned_data['email']
#             request.session['password'] = form.cleaned_data['password']
#             request.session['confirm_password'] = form.cleaned_data['confirm_password']
#             request.session['display_name'] = form.cleaned_data['display_name']
#             request.session['country'] = form.cleaned_data['country']
#             request.session['state'] = form.cleaned_data['state']
#             request.session['city'] = form.cleaned_data['city']
#             request.session['date_of_birth'] = form.cleaned_data['date_of_birth']
#             request.session['gender'] = form.cleaned_data['gender']
#             request.session['heading'] = form.cleaned_data['heading']
#             request.session['country_code'] = form.cleaned_data['country_code']
#             request.session['mobile_number'] = form.cleaned_data['mobile_number']
#             # Redirect to the next step of registration form
#             return redirect('profiles:next_form')

#     else:
#         form = RegisterForm1()

#     return render(request, 'profiles/escort_register.html', {'form': form})


# Client Registration view
def client_register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST, request.FILES)
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
        form = RegisterForm1()
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
