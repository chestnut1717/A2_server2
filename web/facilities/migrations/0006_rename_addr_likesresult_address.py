# Generated by Django 4.2.1 on 2023-05-28 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0005_delete_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likesresult',
            old_name='addr',
            new_name='address',
        ),
    ]