# Generated by Django 4.2.10 on 2024-02-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("discord", "0004_alter_discorduser_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discordrole",
            name="role_id",
            field=models.BigIntegerField(blank=True, unique=True),
        ),
    ]
