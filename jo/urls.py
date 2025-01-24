from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.shortcuts import render

urlpatterns = [  
    path("admin/", admin.site.urls),
    path("", include("sports.urls")),
    path('ticket/', include("ticket.urls")),
    path('connexion/', include("connexion.urls")),
    path('panier/', include("panier.urls"))
]

def page_not_found(request, exception):
    return render(request, "404.html", {'theme' : 'page_not_found.css'}, status=404)

handler404 = page_not_found

def server_error(request):
    return render(request, "500.html", {'theme' : 'page_not_found.css'}, status=500)

handler500 = server_error