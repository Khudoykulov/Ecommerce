from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.account.models import User
from apps.product.models import Product


class Promo(models.Model):
    name = models.CharField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='promos')
    description = models.TextField(null=True, blank=True)
    expire_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    members = models.ManyToManyField(User, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(250000.00)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem,)
    promo = models.CharField(max_length=8, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



