# Generated by Django 4.1 on 2023-04-14 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('user', '0015_alter_role_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='roles', to='auth.permission'),
        ),
    ]