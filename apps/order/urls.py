from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    CartItemViewSet,
    CheckPromo

)

app_name = 'orders'

router = DefaultRouter()
router.register('', OrderViewSet, basename='order')
router.register('cart-item', CartItemViewSet, basename='cart-items')

urlpatterns = [

    path('', include(router.urls)),
    path('check-promo/', CheckPromo.as_view(), name='check-promo')
]
