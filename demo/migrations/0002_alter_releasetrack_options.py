# Generated by Django 5.1.dev20240112204018 on 2024-01-15 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='releasetrack',
            options={'ordering': ['release', 'track_number']},
        ),
    ]
