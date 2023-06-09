# Generated by Django 4.2 on 2023-05-08 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_friendlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friends_list', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
