# Generated by Django 4.1 on 2023-03-30 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0035_rename_loan_id_collateral_loan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guarantor',
            old_name='loan_no',
            new_name='loan',
        ),
    ]