# Generated by Django 4.2 on 2023-05-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_guest',
            field=models.BooleanField(default=False, verbose_name='Guest'),
        ),
    ]
