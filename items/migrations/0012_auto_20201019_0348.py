# Generated by Django 3.0.3 on 2020-10-18 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_remove_category_isaddon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='addOnPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Extra Option Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='option1',
            field=models.BooleanField(default=False),
        ),
    ]
