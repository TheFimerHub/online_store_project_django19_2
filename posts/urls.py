from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore
from django.conf import settings  # type: ignore
from django.conf.urls.static import static  # type: ignore

from posts.apps import PostsConfig
from posts.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView

app_name = PostsConfig.name

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('', PostListView.as_view(), name='index'),
    path('view/<slug:slug>/', PostDetailView.as_view(), name='view'),
    path('update/<slug:slug>/', PostUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', PostDeleteView.as_view(), name='delete'),
]