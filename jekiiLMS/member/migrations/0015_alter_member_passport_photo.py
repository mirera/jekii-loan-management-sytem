# Generated by Django 4.1 on 2023-03-22 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_alter_member_passport_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='passport_photo',
            field=models.ImageField(upload_to=''),
        ),
    ]
