# Generated by Django 4.1 on 2023-04-17 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0045_collateral_company_guarantor_company_note_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collateral',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='collateral',
            name='serial_number',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='collateral',
            name='type',
            field=models.CharField(choices=[('electronics', 'ELECTRONICS'), ('vehicle', 'VEHICLE'), ('land', 'LAND'), ('shares', 'SHARES'), ('cash deposit', 'CASH DEPOSIT'), ('others', 'OTHERS')], default='electronics', max_length=50),
        ),
    ]