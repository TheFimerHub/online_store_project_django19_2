from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from catalog.views import HomePageView, ContactsPageView, ProductDetailView, create_product

urlpatterns = [
    path('', HomePageView.as_view()),
    path('contacts/', ContactsPageView.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view()),
    path('create/', create_product, name='create_product'),
]
