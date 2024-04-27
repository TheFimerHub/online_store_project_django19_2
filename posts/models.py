from django.db import models

from catalog.models import NULLABLE


class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name='title')
    slug = models.CharField()
    content = models.TextField(max_length=2200, verbose_name='content')
    preview = models.ImageField(upload_to='products/', verbose_name='preview', **NULLABLE)
    creation_date = models.DateField(auto_now_add=True, verbose_name='creation date')
    publication_sign = models.BooleanField(default=True, verbose_name='public')
    views = models.IntegerField(default=0, verbose_name='views')

    def get_image_url(self):
        if self.preview:
            return f"posts/{self.preview}"
        return ''

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'