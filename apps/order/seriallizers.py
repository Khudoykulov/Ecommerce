from attr import attrs
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Order, Promo, CartItem, OrderItem
from ..product.models import Product
from ..product.seriallizers import ProductSerializer


class PromoSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user
        name = attrs.get('name')
        if name is None:
            raise ValidationError('detail', 'promo name is required')
        promo = Promo.objects.filter(name=name)
        if not promo.exists():
            raise ValidationError('detail', 'promo does not exist')
        if promo.last().is_expired:
            raise ValidationError('detail', 'Promo is expired')
        if user in promo.last().members.all():
            return ValidationError('detail', 'promo is already expired')
        return attrs

    def create(self, validated_data):
        name = validated_data['name']
        promo = Promo.objects.get(name=name)
        promo.members.add(self.context['request'].user)
        return promo


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'user', 'quantity', 'get_amount', 'created_date']
        read_only_fields = ['get_amount', 'created_date', 'user',]

        extra_kwargs = {
            'product': {'required': False},
            'quantity': {'required': False},
        }


class CartItemPostSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'user', 'quantity', 'get_amount', 'created_date']
        read_only_fields = ['get_amount', 'created_date', 'user',]

        extra_kwargs = {
            'product': {'required': False},
            'quantity': {'required': False},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'user', 'discount', 'quantity', 'unit_price', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'promo', 'amount', 'modified_date', 'created_date', ]


class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'promo', 'amount', 'modified_date', 'created_date', ]
        read_only_fields = ['user', 'items', 'amount', ]

    def create(self, validated_data):
        user = self.context['request'].user
        promo = Promo.objects.filter(name=validated_data['promo'])
        amount = 0
        cart_items = user.cart_items.all()
        order = super().create(validated_data)
        for cart_item in cart_items:
            amount += cart_item.get_amount
            oi = OrderItem.objects.create(
                order=user,
                product_id=cart_item.id,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price,
                discount=cart_item.product.discount,
                amount=cart_item.get_amount
            )
            order.add(oi)
        if promo.exists():
            if promo.last().is_expired:
                raise ValidationError('detail', 'promo is expired')
            if user in promo.first().members.all():
                return ValidationError('detail', 'promo is already expired')
            if promo.min_price > amount:
                return ValidationError('detail', f'Must be more expensive than {promo.min_price}')
            amount = amount * (1 - promo.last().discount/100)
            promo.members.add(user)
        order.amount = amount
        order.save()
        user.cart_items.all().delete()
        return order
