from django.db import models

# Create your models here.
class searchResult(models.Model):
    fileName = models.CharField(max_length=100, null=True)
    webLink = models.CharField(max_length=400, null=True)
    snippet = models.CharField(max_length= 400, null=True)