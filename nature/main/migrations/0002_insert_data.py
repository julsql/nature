# Generated by Django 5.1.4 on 2024-12-23 01:07

from django.db import migrations

from main.core.load_data.add_data import add_data
from main.core.load_data.get_data import get_dataset_on_each_image


def insert_initial_data(apps, schema_editor) -> None:
    info = get_dataset_on_each_image()
    add_data(info)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_initial_data)
    ]
