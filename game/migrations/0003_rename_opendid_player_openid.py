# Generated by Django 3.2.8 on 2022-08-03 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_player_opendid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='opendid',
            new_name='openid',
        ),
    ]
