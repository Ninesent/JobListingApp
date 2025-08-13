from django.urls import path
from hire_hub.accounts import views

urlpatterns = [
    path('profile/', views.company_profile_view, name='profile'),
    path('profile/edit/', views.company_profile_edit, name='profile_edit'),
    path('register/', views.register, name='register'),
    path('register/success/', views.registration_success, name='registration_success'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]


