# Generated by Django 4.2 on 2025-01-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0002_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(default='players/default_image.jpg', upload_to=''),
        ),
    ]
