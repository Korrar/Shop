# Generated by Django 2.2.7 on 2019-11-24 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vat', '0008_auto_20191123_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amount',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='vat.Product'),
        ),
    ]
