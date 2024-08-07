# Generated by Django 4.2.11 on 2024-05-10 12:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_commentimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0004_remove_cartitem_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='is_ordered',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='unit_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_delivered',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='order.orderitem'),
        ),
    ]
