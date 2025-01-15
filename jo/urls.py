from django.contrib import admin
from django.urls import include, path

urlpatterns = [  
    path("admin/", admin.site.urls),
    path("", include("sports.urls")),
    path('ticket/', include("ticket.urls"), name='ticket'),
    path('connexion/', include("connexion.urls"), name='connexion'),
    path('panier/', include("panier.urls"), name='panier')
]
