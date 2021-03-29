from django.db import models

# Create your models here.
class UserExperience(models.Model):
    user=models.CharField(max_length=20)
    feedback=models.CharField(max_length=2000)