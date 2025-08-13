from django.urls import path
from hire_hub.jobs import views

urlpatterns = [

    path('', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/apply/', views.apply_for_job, name='apply_for_job'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('job/create/', views.JobCreateView.as_view(), name='create_job'),
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='delete_job'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_details'),
    path('applications/<int:pk>/schedule_interview/', views.schedule_interview, name='schedule_interview'),
]

