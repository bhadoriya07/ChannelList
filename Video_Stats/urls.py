import imp
from django.urls import path
from Video_Stats.views import *

urlpatterns = [
    path('',showPage),
    path('downloadFile',downloadFile)
]