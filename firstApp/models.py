from pyexpat import model
from django.db import models

class urls(models.Model):
    url = models.TextField(max_length=100)
