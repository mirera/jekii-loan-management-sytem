# Generated by Django 4.1 on 2023-03-03 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0016_alter_loan_application_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='application_date',
            field=models.DateField(),
        ),
    ]
