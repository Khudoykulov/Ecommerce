from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
    TradeViewSet,
    WishlistViewSet
)

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'product'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'', ProductViewSet)
router.register(r'wishlist', WishlistViewSet)

urlpatterns = [
    path('', include(router.urls)),

]

