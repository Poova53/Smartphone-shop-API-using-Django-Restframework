# Generated by Django 4.2.1 on 2023-06-09 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smartphoneShopAPI', '0007_alter_cart_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_items', models.IntegerField()),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[('Y', 'Yet to dispatch'), ('S', 'Shipped'), ('O', 'Out for delivery'), ('D', 'Delivered')], max_length=4)),
                ('ordered_time', models.DateTimeField(auto_now_add=True)),
                ('ordered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_product', to='smartphoneShopAPI.product')),
            ],
        ),
    ]
