# auth/signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import BlogAnonymous  # Import BlogAnonymous here, if needed

# Custom signal handler to handle user login
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Custom logic for user login, e.g., logging, user activity tracking, etc.
    print(f"User {user} logged in.")
    if not user.is_authenticated:
        print("User is not authenticated!")
