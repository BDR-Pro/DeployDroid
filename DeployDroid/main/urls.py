from django.urls import path
from main import views  


urlpatterns = [
    path('install/', views.install_view, name='install'),
]
