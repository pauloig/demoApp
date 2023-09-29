# Generated by Django 4.0.6 on 2023-09-28 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workOrder', '0087_alter_loginaudit_employeeid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='woCommentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('createdBy', models.CharField(blank=True, max_length=60, null=True)),
                ('woID', models.ForeignKey(db_column='woID', on_delete=django.db.models.deletion.CASCADE, to='workOrder.workorder')),
            ],
        ),
    ]
