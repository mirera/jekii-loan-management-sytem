# Generated by Django 4.1 on 2023-03-29 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0034_alter_collateral_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collateral',
            old_name='loan_id',
            new_name='loan',
        ),
    ]
