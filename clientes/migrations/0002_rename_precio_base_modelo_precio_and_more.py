# Generated by Django 5.1.3 on 2024-12-10 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelo',
            old_name='precio_base',
            new_name='precio',
        ),
        migrations.RemoveField(
            model_name='modelo',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='modelo',
            name='nombre',
        ),
        migrations.AddField(
            model_name='modelo',
            name='anio',
            field=models.PositiveIntegerField(default=2000),
        ),
        migrations.AddField(
            model_name='modelo',
            name='modelo',
            field=models.CharField(choices=[('Ford Fiesta', 'Ford Fiesta'), ('Ferrari', 'Ferrari'), ('Lotus', 'Lotus')], default='Ford Fiesta', max_length=255),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='modelo',
            name='marca',
            field=models.CharField(max_length=255),
        ),
    ]