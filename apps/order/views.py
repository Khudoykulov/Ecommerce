from apps.utils.mixins import CreateViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from .models import (
    Order,
    OrderItem,
    Promo,
    CartItem,
)
from .seriallizers import (
    OrderPostSerializer,
    PromoSerializer,
    OrderSerializer,
    ProductSerializer,
    CartItemSerializer,
    OrderItemSerializer,
    CartItemPostSerializer
)


class CheckPromo(generics.ListAPIView):
    serializer_class = PromoSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PromoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(CreateViewSetMixin, viewsets.ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_post_class = OrderPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
