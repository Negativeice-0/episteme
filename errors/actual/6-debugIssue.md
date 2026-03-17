# debug was flagging an error in backend/config urls.py

```bash

also imported reverse in datasets/admin
and added some code in for views so reverse and preview from admin can work.


"""
URL configuration for Episteme project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from datasets import views  # Fix: Remove 'backend.' prefix

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('datasets/<int:id>/preview/', views.dataset_preview, name='dataset-preview'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar - only if installed
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
        ```
