# Generated by Django 3.1.6 on 2021-02-25 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20210225_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='isset_Password',
            field=models.BooleanField(default=False),
        ),
    ]
