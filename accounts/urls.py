from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import register, police_login

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('police-login/', police_login, name='police-login'),
    # path('police-login/', LoginView.as_view(template_name='accounts/police-login.html'), name='police-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]
