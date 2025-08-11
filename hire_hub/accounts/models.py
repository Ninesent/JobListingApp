from django.db import models
from django.contrib.auth.models import User
from hire_hub.jobs.models import Company

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile for {self.company.name if self.company else 'Unassigned'}"
