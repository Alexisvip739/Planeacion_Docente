# Generated by Django 3.2.12 on 2022-09-27 02:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docentes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Actividades',
            new_name='Actividade',
        ),
        migrations.AddField(
            model_name='planeacion',
            name='id_usuario',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]