from django.urls import path

from .views import get_leads

urlpatterns = [
    path('get-leads/<int:pk>/', get_leads, name='get-leads'),
    path('get-leads/<int:pk>/<operation>/', get_leads, name='get-leads'),
]