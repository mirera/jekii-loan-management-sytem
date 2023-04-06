# Generated by Django 4.1 on 2023-04-06 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_organization_phone_no'),
        ('branch', '0017_expense_company_expensecategory_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.organization'),
        ),
        migrations.AlterField(
            model_name='expensecategory',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.organization'),
        ),
    ]
