# Generated by Django 4.1 on 2023-07-12 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0032_remove_smssetting_member_welcome'),
    ]

    operations = [
        migrations.AddField(
            model_name='templatesetting',
            name='loan_applied',
            field=models.TextField(default='Dear member_name, your application is under review'),
        ),
    ]
