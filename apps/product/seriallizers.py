from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import (
    Category,
    Tag,
    Product,
    ProductImage,
    Rank,
    Trade,
    Comment,
    Wishlist
)


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []

    class Meta:
        model = Category
        fields = ['id', 'name', 'order', 'children']





# class TradeSerializer(serializers.ModelSerializer):
#     product = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Trade
#         fields = '__all__'
#         read_only_fields = ['user',]

# class  MiniProductSerializer(serializers.ModelSerializer):

