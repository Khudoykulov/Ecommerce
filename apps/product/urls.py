from .views import CategoryViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'product'
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]

