# Generated by Django 4.2.5 on 2023-09-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analyze_app", "0002_report_fail_reason"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chessgame",
            name="player_color",
            field=models.IntegerField(
                choices=[(0, "white"), (1, "black")],
                help_text="Player's color 0-White, 1-Black",
            ),
        ),
        migrations.AlterField(
            model_name="chessgame",
            name="result",
            field=models.FloatField(
                choices=[(0, "white"), (1, "black"), (0.5, "draw")], max_length=10
            ),
        ),
    ]
