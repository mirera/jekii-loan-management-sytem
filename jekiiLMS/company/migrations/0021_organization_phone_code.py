# Generated by Django 4.1 on 2023-05-24 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0020_organization_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='phone_code',
            field=models.CharField(default='1', max_length=5),
        ),
    ]
