from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
