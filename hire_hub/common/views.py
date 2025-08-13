from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render
from hire_hub.jobs.models import JobPosting, Application


class HomePageView(TemplateView):
    template_name = 'common/homepage.html'


class AboutPageView(TemplateView):
    template_name = 'common/about.html'

@login_required
def dashboard(request):
    job_postings = JobPosting.objects.all().order_by('-posted_date')

    recent_applicants = Application.objects.all().order_by('-submitted_date')[:5]

    context = {
        'job_postings': job_postings,
        'recent_applicants': recent_applicants,
    }

    return render(request, 'common/dashboard.html', context)