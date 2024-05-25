# Generated by Django 5.0.4 on 2024-05-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_usuario_membresia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenador',
            name='especialidad',
            field=models.CharField(choices=[(1, 'Boxeo'), (2, 'Musculación'), (3, 'Zumba'), (4, 'Yoga'), (5, 'Pilates')], default=2, max_length=100),
        ),
    ]