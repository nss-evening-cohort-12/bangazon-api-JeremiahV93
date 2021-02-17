from django.urls import path
from .views import products_over_1000, products_equal_or_less_999

urlpatterns = [
    path('reports/products_over_1000', products_over_1000),
    path('reports/products_under_999', products_equal_or_less_999)
]
