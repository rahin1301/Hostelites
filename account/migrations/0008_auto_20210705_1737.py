# Generated by Django 3.1.7 on 2021-07-05 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20210705_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_order_history',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.order'),
        ),
        migrations.AlterField(
            model_name='shopkeeper_order_history',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.order'),
        ),
    ]