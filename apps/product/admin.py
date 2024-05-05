from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.product.models import (
    Category,
    Tag,
    Product,
    ProductImage,
    Wishlist,
    Trade,
    Rank,
    Like,
    Comment
)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'parent', 'created_date')
    date_hierarchy = 'created_date'
    search_fields = ('id', 'name')


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImageInline]
    list_display = ('id', 'name', 'price', 'discount', 'sold_count', 'category', 'get_available',
                    'get_quantity', 'average_rank', 'category', 'created_date')
    date_hierarchy = 'created_date'
    filter_horizontal = ('tags', )
    search_fields = ('id', 'name')
    list_filter = ('category', 'tags')
    readonly_fields = ('get_available', 'get_quantity', 'average_rank', 'get_lakes', 'modified_date', 'created_date')


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    date_hierarchy = 'created_date'
    search_fields = ('id', 'product__name',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('id', 'product__name', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('id', 'product__name', )


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('id', 'product__name', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'parent', 'top_level_comment_id', 'created_date')
    date_hierarchy = 'created_date'
    search_fields = ('id', 'product__name', )
    list_filter = ('parent', )

