# Generated by Django 4.1 on 2023-07-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0034_templatesetting_loan_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatesetting',
            name='member_welcome',
            field=models.TextField(default='Dear {first_name} {last_name}, welcome to {organization_name}. Access business loans & scale your business.'),
        ),
    ]