from django.db import models
from django.contrib.auth.models import User


JOB_TYPE_CHOICES = (
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Contract', 'Contract'),
    ('Internship', 'Internship'),
)


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_postings')
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='job_postings')
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)


    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Full-time')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    submitted_date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Interviewing', 'Interviewing'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Application from {self.applicant_name} for {self.job_posting.title}"


class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    scheduled_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    INTERVIEW_TYPES = [
        ('Phone Screen', 'Phone Screen'),
        ('Technical', 'Technical'),
        ('Behavioral', 'Behavioral'),
        ('Final', 'Final'),
    ]
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPES, default='Phone Screen')

    def __str__(self):
        return f"{self.interview_type} for {self.application.applicant_name}"
