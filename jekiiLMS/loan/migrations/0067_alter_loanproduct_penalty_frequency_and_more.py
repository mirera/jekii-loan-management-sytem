# Generated by Django 4.1 on 2023-06-05 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0066_remove_loan_amount_mpesa_s'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanproduct',
            name='penalty_frequency',
            field=models.CharField(choices=[('onetime', 'ONETIME'), ('daily', 'DAILY'), ('weekly', 'WEEKLY'), ('monthly', 'MONTHLY')], default='onetime', max_length=300),
        ),
        migrations.AlterField(
            model_name='loanproduct',
            name='penalty_type',
            field=models.CharField(choices=[('fixed_value', 'FIXED VALUE'), ('percentage of due_amount', 'p.c of Due Amount')], default='fixed_value', max_length=300),
        ),
    ]
