# Generated by Django 2.2.28 on 2024-03-12 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('melodyMeter', '0004_album_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
