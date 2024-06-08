from django.urls import path, include
from data.views import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]