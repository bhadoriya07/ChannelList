import imp
from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('exportfile',views.exportfile,name="exportfile")
]
