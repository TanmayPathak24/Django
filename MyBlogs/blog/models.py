from django.db import models

# Create your models here.
import datetime
class Blog(models.Model):
    author_id=models.IntegerField(default=0)
    title=models.CharField(max_length=100, blank=False)
    publish_date=models.DateTimeField(default=datetime.datetime.today())
    content=models.TextField(max_length=5000)
    last_modified=models.DateTimeField(default=datetime.datetime.today())


class Author(models.Model):
    author_name=models.CharField(max_length=50, blank=False)
    avatar=models.CharField(max_length=50, blank=False)
    description=models.TextField()
    password=models.CharField(max_length=20, blank=False, default='admin')