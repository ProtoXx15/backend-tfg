# Generated by Django 5.0.4 on 2024-06-06 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_membresia_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membresia',
            name='duracion',
            field=models.IntegerField(),
        ),
    ]