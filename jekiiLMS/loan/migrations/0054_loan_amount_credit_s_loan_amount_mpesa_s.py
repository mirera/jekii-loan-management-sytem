# Generated by Django 4.1 on 2023-05-02 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0053_alter_mpesastatement_loan'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='amount_credit_s',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='amount_mpesa_s',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
