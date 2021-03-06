# Generated by Django 2.2.7 on 2019-11-23 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vat', '0003_auto_20191123_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_list',
            field=models.ManyToManyField(blank=True, to='vat.Amount'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
