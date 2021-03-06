# Generated by Django 2.2 on 2021-02-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Billing_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('country', models.CharField(blank=True, max_length=70, null=True)),
                ('state', models.CharField(blank=True, max_length=70, null=True)),
                ('city', models.CharField(blank=True, max_length=70, null=True)),
                ('postal', models.CharField(blank=True, max_length=70, null=True)),
                ('name_on_card', models.CharField(max_length=120)),
                ('card_number', models.CharField(max_length=17, unique=True)),
                ('card_cvv', models.CharField(max_length=5)),
                ('card_type', models.CharField(choices=[('credit', 'credit'), ('debit', 'debit')], max_length=6)),
                ('receive_date', models.DateField(auto_now=True)),
                ('used', models.BooleanField(default=False)),
                ('pin', models.BooleanField(default=False)),
                ('usage_date', models.DateTimeField(blank=True, null=True)),
                ('exp', models.DateField(blank=True, max_length=2, null=True)),
            ],
        ),
    ]
