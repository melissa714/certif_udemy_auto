# Generated by Django 4.2.5 on 2023-09-24 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='photo_number',
            new_name='phone_number',
        ),
    ]
