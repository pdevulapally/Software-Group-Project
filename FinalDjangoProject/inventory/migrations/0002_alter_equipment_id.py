# Generated by Django 4.2.11 on 2024-04-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
