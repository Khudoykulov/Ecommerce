from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save
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
    # unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    # is_ordered = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}'

    @property
    def get_amount(self):
        return (float(self.product.price) * ((self.product.discount or 1)/100)) * self.quantity


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='order_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(OrderItem,)
    promo = models.CharField(max_length=8, null=True, blank=True)
    # is_delivered = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


# def cart_item_pre_save(sender, instance, **kwargs):
#     instance.unit_price = instance.product.price
#     if instance.product.discount:
#         amount = (instance.product.discount * instance.unit_price * instance.quantity) / 100
#     else:
#         amount = instance.unit_price * instance.quantity
#     instance.amount = amount
#
#
# def order_pre_save(sender, instance, **kwargs):
#     amount = sum(instance.cart_item.values_list('amount', flat=True))
#     if instance.promo:
#         instance.promo in Promo.objects.values_list('name', flat=True)
