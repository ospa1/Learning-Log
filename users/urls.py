""" url patterns for the users """

from django.urls import path, include
from . import views

# allows django to distinguish these urls from other app's urls
app_name = 'users'

urlpatterns = [
    # default auth urls - login page’s pattern matches http://localhost:8000/users/login/
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]
