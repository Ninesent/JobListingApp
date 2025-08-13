from django.urls import path
from hire_hub.jobs import views

urlpatterns = [

    path('', views.JobPostListView.as_view(), name='job_list'),
    path('job/<int:pk>/', views.JobPostDetailsView.as_view(), name='job_detail'),
    path('post/', views.JobPostingView.as_view(), name='create_job'),
    path('job/<int:pk>/edit/', views.JobEditView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='delete_job'),
    path('job/<int:pk>/apply/', views.JobApplicationView.as_view(), name='apply_for_job'),
    path('application-confirmation/<str:status>/', views.ApplicationConfirmationView.as_view(), name='application_confirmation'),
    path('applicant/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),
    path('applications/<int:application_pk>/schedule_interview/', views.schedule_interview, name='schedule_interview'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail')
]

