from django.urls import path, include
from hire_hub.jobs import views

urlpatterns = [
    path('', views.job_list_view, name='job-list'),
    path('create/', views.create_job_listing, name='create-job'),
    path('/<int:pk>/', include([
        path('update/', views.update_job_listing, name='update-job'),
        path('delete/', views.delete_job_listing, name='delete-job'),
        path('apply/', views.apply_for_job, name='apply-for-job'),
    ]) )
]