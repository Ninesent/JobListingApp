from django.contrib import admin
from hire_hub.jobs.models import Application, Interview, JobCategory


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = ('job_posting', 'applicant_name', 'applicant_email', 'applicant_phone', 'resume')
    list_filter = ('applicant_name', 'job_posting', 'applicant_email')
    search_fields = ('applicant_name', 'applicant_email')
    ordering = ('-applicant_name',)
    readonly_fields = ('resume',)

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = ('application', 'interviewer',)
    list_filter = ('interviewer',)
    search_fields = ('interviewer__username',)
    date_hierarchy = 'scheduled_date'
    ordering = ('-scheduled_date',)

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
