# Generated by Django 4.2.11 on 2024-05-01 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_booking_end_date_alter_booking_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
