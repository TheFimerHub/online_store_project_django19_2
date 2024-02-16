from django.contrib import admin #type: ignore
from django.urls import path #type: ignore
from django.conf import settings #type: ignore
from django.conf.urls.static import static #type: ignore
from catalog.views import home_page, contacts_page, product_detail, create_product

urlpatterns = [
    path('', home_page),
    path('contacts/', contacts_page),
    path('products/<int:product_id>', product_detail),
    path('create/', create_product, name='create_product')
]
