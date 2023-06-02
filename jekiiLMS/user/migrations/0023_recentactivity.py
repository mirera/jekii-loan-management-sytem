# Generated by Django 4.1 on 2023-05-24 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_alter_companystaff_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('loan_approval', 'Loan Approval'), ('loan_rejection', 'Loan Rejection'), ('loan_clearance', 'Loan Clearance'), ('loan_write_off', 'Loan Write-off'), ('loan_roll_over', 'Loan Roll-over'), ('loan_product_addition', 'Loan Product Addition'), ('branch_opened', 'Branch Opened')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(max_length=200)),
            ],
        ),
    ]