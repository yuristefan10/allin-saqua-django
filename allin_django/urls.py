from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
    path(re.sub(r'^/', '', settings.MEDIA_URL) + '<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
