from django.urls import path
from hire_hub.accounts import views

urlpatterns = [
    path('profile/edit/', views.company_profile_edit, name='company_profile_edit'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
