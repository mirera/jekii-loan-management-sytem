# Generated by Django 4.1 on 2023-05-05 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0057_remove_loan_due_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='due_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
