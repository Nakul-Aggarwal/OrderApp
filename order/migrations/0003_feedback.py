# Generated by Django 3.0.3 on 2020-10-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20201013_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, max_length=2000, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
