from django.urls import path
from .views import products_over_1000

urlpatterns = [
    path('reports/products_over_1000', products_over_1000)
]
