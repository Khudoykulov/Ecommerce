# Generated by Django 4.2.11 on 2024-05-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_cartitem_amount_cartitem_discount_order_promo_promo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1123, max_digits=10),
            preserve_default=False,
        ),
    ]
