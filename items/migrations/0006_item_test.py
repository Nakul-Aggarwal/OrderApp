# Generated by Django 3.0.3 on 2020-10-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_item_addon'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]