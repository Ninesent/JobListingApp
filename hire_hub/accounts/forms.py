from django import forms
from hire_hub.jobs.models import Company
from hire_hub.accounts.models import CompanyProfile

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile
        fields = []

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
