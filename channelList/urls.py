import imp
from django.conf import settings
from django.contrib import admin
from django.urls import path
from firstApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('exportfile',views.exportfile,name="exportfile")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
