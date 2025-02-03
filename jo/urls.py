from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
# from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [  
    path("admin/", admin.site.urls),
    path("", include("sports.urls")),
    path('ticket/', include("ticket.urls")),
    path('connexion/', include("connexion.urls")),
    path('panier/', include("panier.urls")), 
    # path('two-factor/', include(tf_urls)),
]

def page_not_found(request, exception):
    return render(request, "404.html", {'theme' : 'page_not_found.css'}, status=404)

handler404 = page_not_found

def server_error(request):
    return render(request, "500.html", {'theme' : 'page_not_found.css'}, status=500)

handler500 = server_error