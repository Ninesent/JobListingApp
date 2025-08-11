from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hire_hub.common.urls')),
    path('accounts/', include('hire_hub.accounts.urls')),
    path('jobs/', include('hire_hub.jobs.urls')),
]
