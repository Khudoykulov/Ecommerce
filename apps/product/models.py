from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
from rest_framework.exceptions import ValidationError

from apps.account.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'      # admindagi nomi uzgartirish
        ordering = ('order', 'id')              #faqat oerimda ishlaydi


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True)
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    views = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_quantity(self):
        incomes = sum(self.trades.filter(action=1).values_list('quantity', flat=True))
        outcomes = sum(self.trades.filter(action=2).values_list('quantity', flat=True))
        return incomes - outcomes

    @property
    def get_available(self):
        return self.get_quantity > 0

    @property
    def average_rank(self):
        try:
             return sum(self.ranks.values_list('rank', flat=True))/(self.ranks.count())
        except ZeroDivisionError:
            return 0

    @property
    def get_lakes(self):
        return self.likes.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product.name


class Trade(models.Model):
    ACTION = (
        (1, _('Income')),
        (2, _('Outcome')),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='trades')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.IntegerField(choices=ACTION, default=1)
    quantity = models.PositiveIntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        incomes = Trade.objects.filter(product_id=self.product_id, action=1).count()
        outcomes = Trade.objects.filter(product_id=self.product_id, action=2).count()
        if outcomes > incomes:
            raise ValidationError('Outcome cannot be more than Income')
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product.name


class Rank(models.Model):
    rank_choice = ((r, r) for r in range(1, 11))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ranks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rank = models.PositiveSmallIntegerField(default=0, choices=rank_choice, db_index=True)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    top_level_comment_id = models.IntegerField(null=True, blank=True, editable=False)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}{self.product.id}->{self.id}'

    @property
    def children(self):
        return Comment.objects.filter(top_level_comment_id=self.id)


class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='comment/%Y/%m/%d', null=True, blank=True)


def comment_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if instance.parent:
            instance.top_level_comment_id = instance.parent.top_level_comment_id
        else:
            instance.top_level_comment_id = instance.id
        instance.save()


post_save.connect(comment_post_save, sender=Comment)

