# Generated by Django 4.2 on 2023-05-10 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_post_share_favorite_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='share',
            unique_together={('user', 'post')},
        ),
    ]
