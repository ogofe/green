# Generated by Django 2.2 on 2021-02-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_information',
            name='pin',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]