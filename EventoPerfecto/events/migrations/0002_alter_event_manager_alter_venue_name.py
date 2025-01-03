# Generated by Django 5.1.2 on 2024-10-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='manager',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Manager Name'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=120, verbose_name='Venue Name'),
        ),
    ]
