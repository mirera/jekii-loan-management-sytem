# Generated by Django 4.1 on 2023-05-23 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0064_loan_interest_amount_loan_service_fee_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loan',
            options={'ordering': ['-application_date'], 'permissions': [('approve_loan', 'Can approve loan'), ('reject_loan', 'Can reject loan'), ('write_off_loan', 'Can write off loan'), ('rollover_loan', 'Can roll over loan')]},
        ),
    ]