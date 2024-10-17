# Generated by Django 5.0.6 on 2024-06-20 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('military_map', '0004_drawing_properties'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='createBy',
        ),
        migrations.RemoveField(
            model_name='point',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='polygon',
            name='createBy',
        ),
        migrations.RemoveField(
            model_name='polygon',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='polyline',
            name='createBy',
        ),
        migrations.RemoveField(
            model_name='polyline',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='rectangle',
            name='createBy',
        ),
        migrations.RemoveField(
            model_name='rectangle',
            name='mission',
        ),
        migrations.DeleteModel(
            name='Circle',
        ),
        migrations.DeleteModel(
            name='Point',
        ),
        migrations.DeleteModel(
            name='Polygon',
        ),
        migrations.DeleteModel(
            name='Polyline',
        ),
        migrations.DeleteModel(
            name='Rectangle',
        ),
    ]
