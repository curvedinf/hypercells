# Generated by Django 4.1.5 on 2023-01-08 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hypercells_api", "0003_context_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="context",
            name="uid",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]