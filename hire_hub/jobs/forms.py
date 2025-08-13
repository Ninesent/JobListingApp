from django import forms
from hire_hub.jobs.models import JobPosting, Application, Interview, JOB_TYPE_CHOICES

class JobPostingForm(forms.ModelForm):
    job_type = forms.ChoiceField(choices=JOB_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))

    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'job_type', 'salary', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'description': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'salary': forms.NumberInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'location': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'cover_letter': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['scheduled_date', 'notes', 'interview_type']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'interview_type': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }
