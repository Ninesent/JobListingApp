from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden

from hire_hub.jobs.models import JobPosting, Application, Interview
from hire_hub.jobs.forms import JobPostingForm, ApplicationForm, InterviewForm


class JobListView(ListView):
    model = JobPosting
    template_name = 'jobs/job_list.html'
    context_object_name = 'job_postings'
    ordering = ['-posted_date']


class JobDetailView(DetailView):

    model = JobPosting
    template_name = 'jobs/job_details.html'
    context_object_name = 'job_posting'


def apply_for_job(request, pk):
    job_posting = get_object_or_404(JobPosting, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_posting = job_posting
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'apply_for_job.html', {'form': form, 'job_posting': job_posting})




class DashboardView(LoginRequiredMixin, ListView):
    model = JobPosting
    template_name = 'jobs/dashboard.html'
    context_object_name = 'company_job_postings'

    def get_queryset(self):
        try:
            company = self.request.user.companyprofile.company
            return JobPosting.objects.filter(company=company).order_by('-posted_date')
        except AttributeError:
            return JobPosting.objects.none()




class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobPosting
    template_name = 'create_job.html'
    form_class = JobPostingForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            form.instance.company = self.request.user.companyprofile.company
        except AttributeError:
            return HttpResponseForbidden("You must have a company profile to post jobs.")
        return super().form_valid(form)



class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = JobPosting
    template_name = 'jobs/edit_job.html'
    form_class = JobPostingForm
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)



class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'jobs/application_details.html'
    context_object_name = 'application'

    def get_queryset(self):
        return Application.objects.filter(job_posting__author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interview_form'] = InterviewForm()
        context['status_choices'] = Application.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_status = request.POST.get('status')
        if new_status and new_status in [choice[0] for choice in Application.STATUS_CHOICES]:
            self.object.status = new_status
            self.object.save()
        return redirect('application_details', pk=self.object.pk)

class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = JobPosting
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('jobs:dashboard')


@login_required
def schedule_interview(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.interviewer = request.user
            interview.save()
            return redirect('application_details', pk=application.pk)
    return redirect('application_details', pk=application.pk)
