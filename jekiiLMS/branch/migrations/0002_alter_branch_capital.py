# Generated by Django 4.1 on 2022-09-06 13:28

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='capital',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
