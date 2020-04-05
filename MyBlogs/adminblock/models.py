from django.db import models

# Create your models here.


class Admin(models.Model):
    admin_name = models.CharField(max_length=50, blank=False)
    avatar = models.CharField(max_length=20, blank=False)
    description = models.TextField()
    password=models.CharField(max_length=50,blank=False)