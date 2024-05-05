from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet
)

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'product'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'', ProductViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),

]

