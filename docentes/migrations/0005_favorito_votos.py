# Generated by Django 3.2.12 on 2022-09-27 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docentes', '0004_auto_20220927_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorito',
            name='votos',
            field=models.IntegerField(default=0),
        ),
    ]
