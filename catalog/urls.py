from django.contrib import admin #type: ignore
from django.urls import path #type: ignore
from django.conf import settings #type: ignore
from django.conf.urls.static import static #type: ignore
from catalog.views import home_page, contacts_page

urlpatterns = [
    path('', home_page),
    path('contacts/', contacts_page)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
