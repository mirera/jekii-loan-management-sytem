# Generated by Django 4.1 on 2023-06-19 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0067_alter_loanproduct_penalty_frequency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='been_penalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.IntegerField(unique=True),
        ),
    ]
