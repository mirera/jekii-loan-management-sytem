# Generated by Django 4.1 on 2023-05-08 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0028_alter_member_previous_credit_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_no',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]