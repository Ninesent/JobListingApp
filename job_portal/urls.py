from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job_portal.common.urls')),
    path('accounts/', include('job_portal.accounts.urls')),
    path('jobs/', include('job_portal.jobs.urls')),
]
