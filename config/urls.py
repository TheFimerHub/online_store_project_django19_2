from django.contrib import admin
from django.urls import path, include

from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('catalog.urls', namespace='catalog')),
  path('post/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
