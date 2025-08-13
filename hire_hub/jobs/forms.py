from django import forms
from django.contrib.auth.models import User

from hire_hub.accounts.models import CompanyProfile
from hire_hub.jobs.models import JobPosting, Application, Interview, JOB_TYPE_CHOICES


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title',
            'category',
            'description',
            'requirements',
            'location',
            'job_type',
            'salary'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_email', 'applicant_phone', 'cover_letter', 'resume']
        widgets = {
            'applicant_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Your full name'
            }),
            'applicant_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'your.email@example.com'
            }),
            'applicant_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'e.g., (123) 456-7890'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Tell us why you are a great fit for this job...',
                'rows': 8
            }),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview

        fields = ['scheduled_date', 'notes', 'interview_type']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class JobEditForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title',
            'description',
            'requirements',
            'job_type',
            'category',
            'location',
            'salary',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Job Title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[150px]',
                'placeholder': 'Detailed job description...',
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 min-h-[150px]',
                'placeholder': 'List of required skills and experience...',
            }),
            'job_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Job Location (e.g., Remote, San Francisco, CA)',
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Salary in USD (e.g., 85000)',
            }),
        }
