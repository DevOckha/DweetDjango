# Generated by Django 4.0.1 on 2022-01-21 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0005_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-id']},
        ),
    ]
