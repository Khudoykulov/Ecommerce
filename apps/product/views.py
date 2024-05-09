from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, views, status, permissions, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.utils.mixins import CreateViewSetMixin
from .permission import IsAdminOrReadOnly, IsAuthor
from apps.product.models import Category, Tag, Product, ProductImage, Trade, Wishlist
from apps.product.seriallizers import (
    CategorySerializer,
    TagSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductPostSerializer,
    TradeSerializer,
    TradePostSerializer,
    WishListSerializer,
    WishListPostSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_object(self):
        queryset = self.queryset
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    serializer_post_class = ProductPostSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'tags']
    ordering_fields = ['views', 'id', 'sold_count']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.serializer_class
        return self.serializer_post_class

    def filter_queryset(self, queryset):
        queryset = super().get_queryset()
        category = Category.objects.all()
        products_category_list = []
        products_category = queryset.filter(category__parent=self.request.query_params.get('category'))
        for c in category:
            if products_category:
                products_category_list.append(products_category)
                return products_category_list
            return queryset
    # def filter_queryset(self, queryset):
    #     parent_category_id = self.request.query_params.get('parent_category_id')
    #     if parent_category_id:
    #         queryset = queryset.filter(parent_id=parent_category_id)
    #     return queryset

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        pid = self.kwargs.get('pid')
        if pid:
            return ProductImage.objects.filter(product_id=pid)
        return ProductImage.objects.none()

    def get_serializer_context(self):
        pid = self.kwargs.get('pid')
        ctx = super().get_serializer_context()
        ctx['pid'] = pid
        return ctx


class TradeViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    model = Trade
    serializer_class = TradeSerializer
    serializer_post_class = TradePostSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['product__name',]
    filterset_fields = ['action', 'product']


class WishlistViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    model = Wishlist
    serializer_class = WishListSerializer
    serializer_post_class = WishListPostSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend,]
    search_fields = ['product__name']
    permission_classes = [IsAuthor | IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)

