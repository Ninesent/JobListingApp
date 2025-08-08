from django.shortcuts import render


def login(request):
    return render(request, 'accounts/login-page.html')


def register(request):
    return render(request, 'accounts/register-page.html')

def logout(request):
    pass

def profile_details(request, pk):
    pass

def profile_edit(request, pk):
    pass

def profile_delete(request, pk):
    pass