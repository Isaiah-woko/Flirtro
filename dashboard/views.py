from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.models import User
from profiles.models import ClientProfile
from django.contrib.auth.decorators import login_required

@login_required
def client_dashboard(request):
    print(f"Requesting profile for user: {request.user}")  # Print the logged-in user

    try:
        profile = ClientProfile.objects.get(user=request.user)
        print(f"Profile found: {profile}")  # Print the profile if found
    except ClientProfile.DoesNotExist:
        print(f"Profile not found for user: {request.user}")  # Print if profile is not found
        raise Http404("Profile not found")
    
    print(f"Rendering template with profile: {profile}")  # Print before rendering the template
    return render(request, 'Dashboard/client_dashboard.html', {'profile': profile})

    