from django.conf import settings
from django.contrib import admin
from django.urls import path
#from firstApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from Video_Stats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.home),
    path('',views.showPage),
    path('downloadFile',views.downloadFile,name="downloadFile")
    #path('exportfile',views.exportfile,name="exportfile")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
