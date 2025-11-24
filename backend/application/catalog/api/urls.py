"""
URL configuration for Products API.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, ToppingViewSet, WrapperViewSet

app_name = 'products'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'toppings', ToppingViewSet, basename='topping')
router.register(r'wrappers', WrapperViewSet, basename='wrapper')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
