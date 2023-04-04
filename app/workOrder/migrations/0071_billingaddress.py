# Generated by Django 4.0.6 on 2023-04-03 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0070_woestimate_address_woestimate_city_woestimate_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='billingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipCode', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('createdBy', models.CharField(blank=True, max_length=60, null=True)),
            ],
        ),
    ]
