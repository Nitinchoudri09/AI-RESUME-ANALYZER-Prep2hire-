from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desired_role = models.CharField(max_length=100)


class Job(models.Model):
    job_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    url = models.URLField()
    date_posted = models.DateTimeField()

    def __str__(self):
        return self.name
