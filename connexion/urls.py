from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

# urlpatterns = [
#   path('', connexion, {'action': 'login'}, name='login'),
#   path('enregistrement/', connexion, {'action': 'signup'}, name='signup'),
#   # path('mot_de_passe/', connexion, {'action': 'password'}, name='password_reset'),
  
#   path('mot_de_passe/', auth_views.PasswordResetView.as_view(template_name="connexion.html"),{'action': 'password'}, name='password_reset'),
#   # path('password_update_done/', auth_views.PasswordResetDoneView.as_view, name='password_update_done'),
#   # path('password_update_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view, name='password_update_confirm'),
#   # path('password_update_complete/', auth_views.PasswordResetCompleteView.as_view, name='password_update_complete'),
  
# ]

urlpatterns = [
    path('', connexion, {'action': 'login'}, name='login'),
    path('enregistrement/', connexion, {'action': 'signup'}, name='signup'),
    
    path('mot_de_passe/', CustomPasswordResetView.as_view(
        template_name="password_reset.html", 
        email_template_name="password_reset_email.html",  
    ), name='password_reset'),

    path('password_reset_done/', CustomPasswordResetDoneView.as_view(template_name="password_reset_done.html",  
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html",  
    ), name='password_reset_confirm'),

    path('reset/done/', CustomPasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html",  
    ), name='password_reset_complete'),
    
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
]

