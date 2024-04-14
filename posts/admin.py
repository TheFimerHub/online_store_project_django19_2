from django.contrib import admin
from posts.models import Post

@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'slug',
                    'content',
                    'preview',
                    'creation_date',
                    'publication_sign',
                    'views',)
