# Generated by Django 4.1 on 2023-05-26 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_alter_organization_phone_no'),
        ('user', '0023_recentactivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='recentactivity',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.organization'),
        ),
    ]