# auth/apps.py

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        # Register any signals here
        from . import signals  # This will ensure signals are registered when the app is ready
