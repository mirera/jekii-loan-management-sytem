# Generated by Django 4.1 on 2023-03-17 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0010_expense_branch_expense_created_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['-expense_date']},
        ),
    ]