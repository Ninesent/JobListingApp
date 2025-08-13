from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from hire_hub.accounts.models import CompanyProfile
import re


class CompanyRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, required=True, label="Company Name")
    company_description = forms.CharField(widget=forms.Textarea, required=True, label="Company Description")
    email = forms.EmailField(required=True, label="Contact Email")
    phone_number = forms.CharField(max_length=20, required=False, label="Contact Phone Number (Optional)")
    website = forms.URLField(required=False, label="Company Website (Optional)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'})

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if CompanyProfile.objects.filter(company_name=company_name).exists():
            raise ValidationError("A company with this name already exists. Please choose a different name.")
        return company_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CompanyProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already associated with another company profile.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_regex = re.compile(r'^\+?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
            if not phone_regex.match(phone_number):
                raise forms.ValidationError("Please enter a valid phone number (e.g., +1 (555) 555-5555).")
            if CompanyProfile.objects.filter(phone_number=phone_number).exists():
                raise ValidationError("This phone number is already associated with another company profile.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        company_name = self.cleaned_data.get('company_name')
        company_description = self.cleaned_data.get('company_description')
        website = self.cleaned_data.get('website')
        email = self.cleaned_data.get('email')
        phone_number = self.cleaned_data.get('phone_number')

        CompanyProfile.objects.create(
            user=user,
            company_name=company_name,
            description=company_description,
            website=website,
            email=email,
            phone_number=phone_number
        )

        return user


class CompanyProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Contact Email")
    phone_number = forms.CharField(max_length=20, required=False, label="Contact Phone Number (Optional)")

    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'description', 'website', 'email', 'phone_number']
        labels = {
            'company_name': 'Company Name',
            'description': 'Company Description',
            'email': 'Contact Email',
            'website': 'Company Website (Optional)',
            'phone_number': 'Contact Phone Number (Optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
            })

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if CompanyProfile.objects.exclude(pk=self.instance.pk).filter(company_name=company_name).exists():
            raise ValidationError("A company with this name already exists. Please choose a different name.")
        return company_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CompanyProfile.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already associated with another company profile.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_regex = re.compile(r'^\+?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$')
            if not phone_regex.match(phone_number):
                raise forms.ValidationError("Please enter a valid phone number (e.g., +1 (555) 555-5555).")
            if CompanyProfile.objects.exclude(pk=self.instance.pk).filter(phone_number=phone_number).exists():
                raise ValidationError("This phone number is already associated with another company profile.")
        return phone_number
