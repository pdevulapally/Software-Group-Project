# Generated by Django 4.2.11 on 2024-04-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='adminApprovalStatus',
            field=models.BooleanField(default=False),
        ),
    ]