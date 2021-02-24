from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from . import rest

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('api/loginGoogle', rest.GoogleLoginView.as_view(), name='login-google'),

]