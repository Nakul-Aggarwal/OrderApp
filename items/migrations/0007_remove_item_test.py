# Generated by Django 3.0.3 on 2020-10-15 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_item_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='test',
        ),
    ]
