# Generated by Django 4.0.6 on 2023-01-09 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0035_alter_internalpo_pickupemployee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='approvedBy',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='period',
            name='approved_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='period',
            name='closedBy',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='period',
            name='closed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
