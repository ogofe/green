# Generated by Django 2.2 on 2021-02-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_information',
            name='country',
            field=models.CharField(blank=True, default='United States', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='billing_information',
            name='exp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='unique_id',
            field=models.CharField(default='a7poocud0jgw', max_length=12, unique=True),
        ),
    ]
