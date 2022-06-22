from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(('organizations.urls', 'organizations'), namespace='organizations')),
    path('api/v1/', include(('projects.urls', 'projects'), namespace='projects')),
    path('api/user/', include('drf_user.urls')),
]
