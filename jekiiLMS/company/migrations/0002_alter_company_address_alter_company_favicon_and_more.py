# Generated by Django 4.1 on 2023-04-03 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='favicon',
            field=models.ImageField(default='default.png', upload_to='companies_logo/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(default='default.png', upload_to='companies_logo/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(default='Loginit Credits Ltd', max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='phone_no',
            field=models.CharField(default='0712345678', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='site_title',
            field=models.CharField(default='Lending to the unlendable', max_length=100),
        ),
    ]
