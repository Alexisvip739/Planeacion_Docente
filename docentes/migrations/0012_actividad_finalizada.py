# Generated by Django 4.1.1 on 2022-09-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docentes', '0011_alter_favorito_fecha_agregad'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='finalizada',
            field=models.BooleanField(default=False),
        ),
    ]
