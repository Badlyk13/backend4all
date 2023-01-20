from django.urls import path

from .views import beeline

urlpatterns = [
    path('alfanet/<int:pk>/beeline/', beeline, name='alfanet_beeline'),
]