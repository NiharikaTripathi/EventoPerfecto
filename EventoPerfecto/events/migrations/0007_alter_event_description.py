# Generated by Django 5.1.2 on 2024-10-28 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_venue_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=200, verbose_name='Event Description'),
        ),
    ]