# Generated by Django 3.1.7 on 2021-07-03 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_shopkeeper_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopkeeper',
            name='favourite_restaurants',
            field=models.ManyToManyField(blank=True, to='account.Customer'),
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Description', models.TextField()),
                ('Price', models.IntegerField()),
                ('Category', models.CharField(blank=True, max_length=25, null=True)),
                ('favourite_items', models.ManyToManyField(blank=True, to='account.Customer')),
                ('user1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.shopkeeper')),
            ],
        ),
    ]
