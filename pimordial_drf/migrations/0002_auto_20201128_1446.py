# Generated by Django 3.0.7 on 2020-11-28 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pimordial_drf', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserInfo',
        ),
    ]