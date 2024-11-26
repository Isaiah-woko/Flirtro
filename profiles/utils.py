# auth/utils.py

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

# Customizing AnonymousUser if needed
class BlogAnonymous(AnonymousUser):
    def __init__(self):
        self.username = 'Guest'


# Override user loader to handle user retrieval
def load_user(userid):
    User = get_user_model()
    try:
        return User.objects.get(id=userid)
    except User.DoesNotExist:
        return None
