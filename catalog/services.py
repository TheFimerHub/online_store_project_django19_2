from django.core.cache import cache
from .models import Category


def get_categories():
    categories = cache.get('categories')

    if categories is not None:
        return categories

    categories = Category.objects.all()
    cache.set('categories', categories, timeout=900)

    return categories
