from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from hire_hub.jobs.models import Company
from hire_hub.accounts.models import CompanyProfile
from hire_hub.accounts.forms import CompanyProfileForm, CompanyForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('jobs:dashboard')

@login_required
def company_profile_edit(request):
    try:
        profile = request.user.companyprofile
    except ObjectDoesNotExist:
        profile = CompanyProfile.objects.create(user=request.user)

    try:
        company = profile.company
    except ObjectDoesNotExist:
        company = None

    if request.method == 'POST':
        profile_form = CompanyProfileForm(request.POST, instance=profile)
        company_form = CompanyForm(request.POST, instance=company)

        if profile_form.is_valid() and company_form.is_valid():
            profile = profile_form.save()
            company = company_form.save()

            if profile.company is None or profile.company != company:
                profile.company = company
                profile.save()

            return redirect('company_profile_edit')
    else:
        profile_form = CompanyProfileForm(instance=profile)
        company_form = CompanyForm(instance=company)

    context = {
        'profile_form': profile_form,
        'company_form': company_form,
    }
    return render(request, 'accounts/company_profile_edit.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')
