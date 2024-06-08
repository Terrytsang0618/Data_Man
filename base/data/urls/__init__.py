from django.urls import path, include
from data import views

app_name = "data"

urlpatterns = [
    path('', include('data.urls.urls')),
]