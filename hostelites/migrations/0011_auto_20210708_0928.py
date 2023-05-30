# Generated by Django 3.1.7 on 2021-07-08 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hostelites', '0010_auto_20210708_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer_order_history',
            name='order',
        ),
        migrations.AddField(
            model_name='customer_order_history',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='hostelites.OrderItem'),
        ),
        migrations.AddField(
            model_name='customer_order_history',
            name='shopkeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hostelites.shopkeeper'),
        ),
    ]