# Generated by Django 4.1 on 2023-03-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0017_alter_member_passport_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='passport_photo',
            field=models.ImageField(default='/Users/enigma/Desktop/JekiiLMS/jekii-loan-management-sytem/jekiiLMS/static/media/default.png', upload_to='member_passports/'),
        ),
    ]