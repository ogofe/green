# Generated by Django 2.2 on 2021-02-03 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210203_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='billing_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Billing_Information'),
        ),
    ]
