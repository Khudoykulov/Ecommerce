
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, views, status, permissions, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.utils.mixins import CreateViewSetMixin
from .permission import IsAdminOrReadOnly, IsAuthor
from apps.product.models import Category, Tag, Product, ProductImage, Trade, Wishlist, Rank, Like, Comment, CommentImage

from apps.product.seriallizers import (
    CategorySerializer,
    TagSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductPostSerializer,
    TradeSerializer,
    TradePostSerializer,
    WishListSerializer,
    WishListPostSerializer,
    LikeSerializer,
    LikePostSerializer,
    RankSerializer,
    CommentSerializer,
    CommentImageSerializer
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
        if self.request.user.is_superuser:
            return qs.all()
        return qs.filter(user_id=self.request.user.id)


class LikeViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    model = Like
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    serializer_post_class = LikePostSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend,]
    search_fields = ['product__name']
    permission_classes = [IsAuthor | IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs.all()
        return qs.filter(user_id=self.request.user.id)


class RankViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend,]
    search_fields = ['product__name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Rank.objects.all()
        return Rank.objects.none()

    def get_context_data(self, **kwargs):
        ctx = super().get_serializer_context()
        ctx['pid'] = self.kwargs.get('pid')
        return ctx


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent__isnull=True,)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['pid'] = self.kwargs.get('pid')
        return ctx

    def update(self, request, *args, **kwargs):
        pass

    # def get_queryset(self):
    #     pid = self.kwargs.get('pid')
    #     print(pid)
    #     if pid:
    #         queryset = Comment.objects.filter(product_id=pid, parent__isnull=True)
    #         return queryset
    #     return Comment.objects.none()

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
        obj: object = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

