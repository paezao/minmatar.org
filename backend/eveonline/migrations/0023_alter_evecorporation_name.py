# Generated by Django 4.2.10 on 2024-02-15 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("eveonline", "0022_alter_evecorporation_ceo_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evecorporation",
            name="name",
            field=models.CharField(
                blank=True, default="Unknown Corporation", max_length=255
            ),
            preserve_default=False,
        ),
    ]
