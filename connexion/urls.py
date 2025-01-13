from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', connexion, {'action': 'login'}, name='login'),
  path('enregistrement/', connexion, {'action': 'signup'}, name='signup'),
  path('mot_de_passe/', auth_views.PasswordResetView.as_view(), {'action': 'password'}, name='password_reset'),
  
  
  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
  path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
