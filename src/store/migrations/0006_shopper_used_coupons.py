# Generated by Django 2.2 on 2021-02-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopper',
            name='used_coupons',
            field=models.ManyToManyField(blank=True, to='store.Discount'),
        ),
    ]
