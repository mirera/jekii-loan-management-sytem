# Generated by Django 4.1 on 2023-05-11 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0061_alter_loan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='parent_loan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='loan.loan'),
        ),
    ]
