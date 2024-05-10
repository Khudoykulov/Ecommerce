from .views import (
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
    ProductImageViewSet,
    TradeViewSet,
    WishlistViewSet,
    LikeViewSet,
    RankViewSet,
    CommentViewSet,
)

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'product'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'(?P<pid>[0-9]+)/images', ProductImageViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'wishlist', WishlistViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'(?P<pid>[0-9]+)/ranks', RankViewSet)
router.register(r'(?P<pid>[0-9]+)/comments', CommentViewSet)
router.register(r'', ProductViewSet)
urlpatterns = [
    path('', include(router.urls)),

]

