from django.contrib.auth import views as auth_views
from django.urls import include, path
from django_registration.backends.activation.views import RegistrationView

from .forms import CustomRegistrationForm
from .views import CustomPasswordResetView, profile

urlpatterns = [
    # django_registration
    # register/complete/ [name=django_registration_complete, registration_complete.html]
    # activate/<activation_key>/ [name=django_registration_activate, activation_complete.html|activation_failed.html]
    path('register/',
         RegistrationView.as_view(form_class=CustomRegistrationForm,
                                  template_name='django_registration/registration_form.html'),
         name='django_registration_register'),
    path('', include('django_registration.backends.activation.urls')),

    # registration
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         CustomPasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),

    path('profile/', profile, name='profile'),
]
