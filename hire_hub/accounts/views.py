from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy

from hire_hub.accounts.models import CompanyProfile
from hire_hub.accounts.forms import CompanyRegistrationForm, CompanyProfileEditForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


@login_required
def company_profile_edit(request):
    try:
        profile = request.user.companyprofile
    except ObjectDoesNotExist:
        profile = CompanyProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = CompanyProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CompanyProfileEditForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'accounts/company_profile_edit.html', context)


def register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
    else:
        form = CompanyRegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def company_profile_view(request):
    try:
        profile = request.user.companyprofile
    except ObjectDoesNotExist:
        return redirect('register')

    context = {
        'profile': profile,
    }

    return render(request, 'accounts/company_profile.html', context)

def registration_success(request):
    return render(request, 'accounts/registration_success.html')