# Generated by Django 4.1.8 on 2023-10-24 09:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("analyze_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="professional",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]