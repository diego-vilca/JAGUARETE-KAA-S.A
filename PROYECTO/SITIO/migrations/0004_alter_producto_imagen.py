# Generated by Django 3.2.4 on 2021-07-06 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SITIO', '0003_rename_descripcion_producto_descripcion_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]