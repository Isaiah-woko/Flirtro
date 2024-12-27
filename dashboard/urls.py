from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    
]
