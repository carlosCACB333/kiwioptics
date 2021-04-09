from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .forms import AccountAutenticateForm
from . import views
from . import rest


app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', rest.LogoutUser.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('employeeUpdate/<pk>/', views.EmployeeUserUpdateView.as_view(), name='employeeUpdate'),
    path('opticUpdate/<pk>/', views.OpticUserUpdateView.as_view(), name='opticUpdate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html',redirect_authenticated_user=True,form_class=AccountAutenticateForm), name='login'),
    path('valivateEmail/<id>/<codigo>/',views.ValidateEmail.as_view(),name='validateEmail'),
    path('google/', views.RegisterGoogleUserCreateView.as_view(), name='google'),
    path('userOfOptic/', views.UserOfOpticCreateView.as_view(), name='userOfOptic'),
    path('userOfOpticDelete/<id>/', views.UserOfOpticDeleteView.as_view(), name='userOfOpticDelete'),

    #api rest framework
    path('api/loginGoogle', rest.GoogleLoginValidateView.as_view(), name='login-google'),
    path('api/registerGoogle', rest.GoogleLRegisterView.as_view(), name='register-google'),
     path('api/pictureUpdate/<pk>/', rest.PictureUpdateAPIView.as_view(),name='rest-picture-update'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)