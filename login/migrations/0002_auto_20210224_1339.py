# Generated by Django 3.1.6 on 2021-02-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='exipiry_time',
            field=models.DateTimeField(),
        ),
    ]
