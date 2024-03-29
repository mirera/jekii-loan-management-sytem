# Generated by Django 4.1 on 2023-02-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0009_alter_loan_interest_rate_alter_loan_loan_term_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanproduct',
            name='interest_rate_per',
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='loan_term_period',
            field=models.CharField(choices=[('day', 'DAY'), ('week', 'WEEK'), ('month', 'MONTH'), ('year', 'YEAR')], default='month', max_length=20),
        ),
        migrations.AddField(
            model_name='loanproduct',
            name='status',
            field=models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='inactive', max_length=10),
        ),
    ]
