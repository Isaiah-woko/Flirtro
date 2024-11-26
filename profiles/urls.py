from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('escort-register/', views.escort_register, name='escort_register'),
    path('client-register/', views.client_register, name='client_register'),
]
