# Generated by Django 4.1 on 2023-05-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_alter_organization_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.CharField(default='SomeStreet', max_length=100),
        ),
    ]
