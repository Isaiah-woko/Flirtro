from django.urls import path
from profiles import views


app_name = 'profiles'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('escort-register/step1/', views.escort_register1, name='escort_register1'),
    path('escort-register/step2/', views.escort_register2, name='escort_register2'),
    path('escort-register/step3/', views.escort_register3, name='escort_register3'),
    path('client-register/', views.client_register, name='client_register'),
]
