from django import views
from django.db import models

class stats(models.Model):
    videoLink = models.TextField(max_length=100)
    brand = models.CharField(max_length=50)
    brand_category = models.CharField(max_length=50)
    cm_name = models.CharField(max_length=20)
    cost = models.CharField(max_length=10)
    live_date = models.CharField(max_length=10)
    inf_name = models.CharField(max_length=20)
    channel_link = models.TextField(max_length=100)
    inf_category = models.CharField(max_length=10)
    video_duration = models.CharField(max_length=10)
    views_count = models.CharField(max_length=10)
    cost_perviews = models.CharField(max_length=10)
    comments = models.CharField(max_length=10)
    video_title = models.TextField(max_length=200)

