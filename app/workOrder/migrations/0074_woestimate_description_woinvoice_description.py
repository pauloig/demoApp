# Generated by Django 4.0.6 on 2023-04-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0073_billingaddress_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='woestimate',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='woinvoice',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
