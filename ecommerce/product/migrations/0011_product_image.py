# Generated by Django 4.1.3 on 2022-12-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_cart_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='products'),
        ),
    ]
