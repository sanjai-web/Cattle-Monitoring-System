from django.contrib import admin
from django.urls import path, include  # Import 'path' and 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),  
]
