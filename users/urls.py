from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from . import rest

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', rest.LogoutUser.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('employeeUpdate/<pk>/', views.EmployeeUserUpdateView.as_view(), name='employeeUpdate'),
    path('opticUpdate/<pk>/', views.OpticUserUpdateView.as_view(), name='opticUpdate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True), name='login'),
    path('google/', views.RegisterGoogleUserCreateView.as_view(), name='google'),
    path('api/loginGoogle', rest.GoogleLoginValidateView.as_view(), name='login-google'),
    path('api/registerGoogle', rest.GoogleLRegisterView.as_view(), name='register-google'),
]