# Generated by Django 4.1 on 2022-09-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
                ('id_no', models.CharField(max_length=500)),
                ('phone_no', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('business_type', models.TextField()),
            ],
        ),
    ]
