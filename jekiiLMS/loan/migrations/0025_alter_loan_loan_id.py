# Generated by Django 4.1 on 2023-03-20 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0024_alter_loan_options_alter_loan_loan_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
