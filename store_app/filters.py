import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    product_price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = {
            'article_number':['exact'],
            'category':['exact'],
            'product_price':['gt', 'lt']
        }
