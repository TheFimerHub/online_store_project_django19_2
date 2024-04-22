from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore
from posts.apps import PostsConfig
from catalog.views import HomePageView, ContactsPageView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = PostsConfig.name


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('contacts/', ContactsPageView.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete')
]
