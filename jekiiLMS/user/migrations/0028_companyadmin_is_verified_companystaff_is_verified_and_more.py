# Generated by Django 4.1 on 2023-07-09 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_notification_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyadmin',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='companystaff',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='companystaff',
            name='phone_no',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
