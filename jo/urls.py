from django.contrib import admin
from django.urls import include, path

urlpatterns = [  
    path("admin/", admin.site.urls),
    path("", include("sports.urls")),
    path('ticket/', include("ticket.urls")),
    path('connexion/', include("connexion.urls")),
    path('panier/', include("panier.urls"))
]
