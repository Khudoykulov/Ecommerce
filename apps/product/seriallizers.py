from rest_framework import serializers
from .models import (
    Category,
    Tag,
    Product,
    ProductImage,
    Rank,
    Trade,
    Comment,
    Wishlist,
    Like,
    CommentImage
)
from ..account.seriallizers import UserProfileSerializer


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
    category = GetCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

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


class MiniProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = GetCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'description', 'views', 'images', 'average_rank',
                  'get_quantity', 'get_lakes', 'average_rank', 'created_date',
                  'modified_date']
        read_only_fields = ['views', 'created_date', 'modified_date']


class TradeSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)
    action_name = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = Trade
        fields = ['id', 'product', 'user', 'action_name', 'quantity', 'description', 'created_date', 'modified_date']
        read_only_fields = ['user',]


class TradePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ['id', 'product', 'user', 'action', 'quantity', 'description', 'created_date', 'modified_date']
        read_only_fields = ['user',]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class WishListSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'user']


class WishListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'product', 'user']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'product',]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return super().create(validated_data)


class RankSerializer(serializers.ModelSerializer):
    product = MiniProductSerializer(read_only=True)

    class Meta:
        model = Rank
        fields = ['id', 'product', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        pid = self.context['pid']
        validated_data['product_id'] = pid
        return super().create(validated_data)


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = ['id', 'image']

    def create(self, validated_data):
        validated_data['comment_id'] = self.context['comment_id']
        return super().create(validated_data)


class MiniCommentSerializer(serializers.ModelSerializer):
    images = CommentImageSerializer(many=True,)

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'user', 'comment', 'images', 'created_date']


class CommentSerializer(serializers.ModelSerializer):
    images = CommentImageSerializer(many=True,)
    user = UserProfileSerializer(read_only=True)
    tree = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_children(self, obj):
        if obj.parent is None:
            return MiniCommentSerializer(obj.tree.exclude(id=obj.id), many=True).data
        return []

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'user', 'comment', 'images', 'top_level_comment_id', 'tree', 'created_date']
        read_only_fields = ['tree',]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        validated_data['user_id'] = self.context['request'].user.id
        validated_data['product_id'] = self.context['pid']
        obj = super().create(validated_data)
        for image in images:
            CommentImage.objects.create(comment=obj, image=image['image'],)
        return obj
