from django.urls import path

from job_portal.common import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]