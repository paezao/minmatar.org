# Generated by Django 4.2.10 on 2024-02-15 15:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("eveonline", "0020_alter_evecharacter_character_id_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EveCorporationApplication",
        ),
    ]
