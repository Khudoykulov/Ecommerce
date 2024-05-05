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


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']
        extra_kwargs = {'image': {'required': False}}

    def create(self, validated_data):
        pid = validated_data('id')
        validated_data['product_id'] = pid
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = GetCategorySerializer( read_only=True)
    tags = TagSerializer( many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'discount', 'views', 'images',
                  'tags', 'average_rank', 'get_quantity', 'get_lakes', 'average_rank', 'created_date', 'modified_date']
        read_only_fields = ['views', 'created_date', 'modified_date']


class ProductPostSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description', 'discount', 'images',
                  'tags',]
        read_only_fields = ['views', 'created_date', 'modified_date']

        def create(self, validated_data):
            images = validated_data.pop('images', [])
            obj = Product.objects.create(**validated_data)
            for image in images:
                ProductImage.objects.create(product=obj, image=image['image'])
            return obj

        def update(self, instance, validated_data):
            images = validated_data.pop('images', [])
            return super().update(instance, validated_data)

















# class TradeSerializer(serializers.ModelSerializer):
#     product = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Trade
#         fields = '__all__'
#         read_only_fields = ['user',]

# class  MiniProductSerializer(serializers.ModelSerializer):

