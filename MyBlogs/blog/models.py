from django.db import models

# Create your models here.
class Blog(models.Model):
    author=models.CharField(max_length=25, blank=False)
    title=models.CharField(max_length=100, blank=False)
    publish_date=models.DateField(blank=False)
    content=models.TextField(max_length=5000, default="No Content")