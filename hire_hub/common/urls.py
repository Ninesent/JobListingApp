from django.urls import path

from hire_hub.common import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]