# Generated by Django 4.1 on 2023-05-12 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_mpesasetting_emailsetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailsetting',
            name='port',
        ),
    ]