# Generated by Django 3.2.12 on 2023-01-03 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=60)),
                ("last_name", models.CharField(max_length=60)),
                ("company_name", models.CharField(max_length=200)),
                ("address", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("county", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=2)),
                ("zip", models.CharField(max_length=5)),
                ("phone1", models.CharField(max_length=12)),
                ("phone2", models.CharField(max_length=12)),
                ("email", models.CharField(max_length=200)),
                ("web", models.CharField(max_length=400)),
            ],
        ),
    ]
