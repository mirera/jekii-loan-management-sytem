# Generated by Django 4.1 on 2023-04-26 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0050_alter_loan_application_date_alter_loan_approved_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repayment',
            name='loan_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repayments', to='loan.loan'),
        ),
    ]
