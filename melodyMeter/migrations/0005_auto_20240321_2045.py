# Generated by Django 2.2.28 on 2024-03-21 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melodyMeter', '0004_album_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
