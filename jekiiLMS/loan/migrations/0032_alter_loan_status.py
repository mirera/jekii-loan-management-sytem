# Generated by Django 4.1 on 2023-03-28 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0031_alter_guarantor_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('approved', 'APPROVED'), ('rejected', 'REJECTED'), ('overdue', 'OVERDUE'), ('cleared', 'CLEARED')], default='pending', max_length=50),
        ),
    ]