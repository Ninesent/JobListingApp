from django.db import models
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='companyprofile'
    )

    company_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.user.username}'s Company Profile"
