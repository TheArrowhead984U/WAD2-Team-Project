# Generated by Django 4.2.11 on 2024-03-22 01:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("melodyMeter", "0015_alter_album_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="bio",
            field=models.TextField(blank=True, max_length=256),
        ),
    ]
