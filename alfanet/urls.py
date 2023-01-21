from django.urls import path

from .views import beeline, test, upload_mts_csv

urlpatterns = [
    path('alfanet/<int:pk>/beeline/', beeline, name='alfanet_beeline'),
    path('test/', test, name='test_trtre'),
    path('alfanet/<int:pk>/mts/', upload_mts_csv, name='alfanet_mts'),
]