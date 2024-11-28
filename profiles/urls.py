from django.urls import path
from profiles import views
from .views import MultiStepFormWizard

app_name = 'profiles'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('form/', MultiStepFormWizard.as_view(), name='multi_step_form'),
    path('form/complete/', views.form_complete, name='form_complete'),
    path('client-register/', views.client_register, name='client_register'),
]
