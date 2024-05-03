from django.db import models
from django.db.models.signals import pre_save

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
    views = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_quantity(self):
        incomes = self.trades.filter(quantity=1).count()
        outcomes = self.trades.filter(quantity=2).count()
        return incomes - outcomes

    @property
    def get_available(self):
        return self.get_quantity > 0

    @property
    def average_rank(self):
        return sum(self.ranks.values_list('rank', flat=True))/(self.ranks.count())

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
    top_level_comment_id = models.IntegerField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def children(self):
        return Comment.objects.filter(top_level_comment_id=self.id)


def pre_save_comment(self, sender, instance, *args, **kwargs):
    if instance.comment:
        instance.top_level_comment_id = instance.parent.top_level_comment_id
    else:
        instance.top_level_comment_id = instance.id


pre_save.connect(pre_save_comment, sender=Comment)

