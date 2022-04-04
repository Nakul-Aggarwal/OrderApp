# Generated by Django 3.0.3 on 2020-10-18 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0007_remove_item_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='spice',
        ),
        migrations.AddField(
            model_name='menu',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='menu', to='items.Option1'),
        ),
    ]
