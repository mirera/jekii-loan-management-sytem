# Generated by Django 4.1 on 2023-04-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0019_alter_branch_email_alter_branch_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='status',
            field=models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='active', max_length=10),
        ),
    ]
