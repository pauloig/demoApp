# Generated by Django 4.0.6 on 2023-04-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0071_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
