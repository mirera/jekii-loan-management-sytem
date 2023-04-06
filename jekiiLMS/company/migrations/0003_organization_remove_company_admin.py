# Generated by Django 4.1 on 2023-04-05 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_alter_company_address_alter_company_favicon_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.CharField(default='0712345678', max_length=10, unique=True)),
                ('logo', models.ImageField(default='default.png', upload_to='companies_logo/')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(default='SomeStreet 123', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='admin',
        ),
    ]