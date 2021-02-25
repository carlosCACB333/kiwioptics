from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from . import rest

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', rest.LogoutUser.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('api/loginGoogle', rest.GoogleLoginValidateView.as_view(), name='login-google'),
    path('api/registerGoogle', rest.GoogleLRegisterView.as_view(), name='register-google'),

]