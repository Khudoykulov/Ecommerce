from django.shortcuts import render
from rest_framework import generics, views, status, permissions, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permission import IsAdminOrReadOnly
from apps.product.models import Category
from apps.product.seriallizers import (
    CategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)

