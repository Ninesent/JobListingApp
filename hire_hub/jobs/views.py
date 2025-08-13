from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from hire_hub.accounts.models import CompanyProfile
from hire_hub.jobs.models import JobPosting, Application, Interview
from hire_hub.jobs.forms import JobPostingForm, ApplicationForm, InterviewForm, JobEditForm


class JobPostListView(ListView):
    model = JobPosting
    template_name = 'jobs/job_list.html'
    ordering = ['-posted_date']
    context_object_name = 'jobs'


class JobPostDetailsView(DetailView):
    model = JobPosting
    template_name = 'jobs/job_details.html'


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


class JobPostingView(LoginRequiredMixin, CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        try:
            company = self.request.user.companyprofile

            job_posting = form.save(commit=False)
            job_posting.author = self.request.user
            job_posting.company = company
            job_posting.save()

            return super().form_valid(form)

        except ObjectDoesNotExist:
            return redirect('register')


class JobEditView(UserPassesTestMixin, UpdateView):
    model = JobPosting
    form_class = JobEditForm
    template_name = 'jobs/edit_job.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.author


class JobApplicationView(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'jobs/apply_for_job.html'

    def form_valid(self, form):
        job_posting = get_object_or_404(JobPosting, pk=self.kwargs['pk'])
        applicant_email_normalized = form.instance.applicant_email.lower()
        existing_application = Application.objects.filter(
            job_posting=job_posting,
            applicant_email=applicant_email_normalized
        ).exists()

        if existing_application:
            return redirect(reverse('application_confirmation', kwargs={'status': 'duplicate'}))
        else:
            application = form.save(commit=False)
            application.job_posting = job_posting
            application.applicant_email = applicant_email_normalized
            application.save()
            return redirect(reverse('application_confirmation', kwargs={'status': 'success'}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_posting'] = get_object_or_404(JobPosting, pk=self.kwargs['pk'])
        return context


class JobDeleteView(UserPassesTestMixin, DeleteView):
    model = JobPosting
    template_name = 'jobs/job_delete.html'

    success_url = reverse_lazy('job_list')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.author


@login_required
def schedule_interview(request, application_pk):
    application = get_object_or_404(Application, pk=application_pk)

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.interviewer = request.user
            interview.save()


            return redirect(reverse('application_detail', kwargs={'pk': application.pk}))
    else:
        form = InterviewForm()

    return render(request, 'jobs/schedule_interview.html', {'form': form, 'application': application})


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    interview = Interview.objects.filter(application=application).order_by('-scheduled_date').first()

    context = {
        'application': application,
        'interview': interview,
    }
    return render(request, 'jobs/application_detail.html', context)




class ApplicationConfirmationView(TemplateView):
    template_name = 'jobs/application_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status = self.kwargs.get('status', 'unknown')
        context['status'] = status

        return context


class ApplicantDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'jobs/applicant_detail.html'
    context_object_name = 'applicant'

    def get_object(self, queryset=None):
        applicant = super().get_object(queryset)

        if applicant.job_posting.company.user != self.request.user:
            raise Http404

        return applicant
