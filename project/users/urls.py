from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LoginView, LogoutView

from .  import views

app_name = 'users'

urlpatterns = [
    path('singup/' , views.signup , name = 'singup'),
    path('login/' , LoginView.as_view(template_name='profile/login.html'), name= 'user_login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('account/', views.SettingView.as_view() , name='account'),
    path('account/change_password/', views.PasswordChange.as_view(), name="password_change"),

    path('team-work/' , views.TeamWorkView.as_view() , name='teamwork'),
    path('partners/' , views.PartnersView.as_view() , name='partners'),
]
