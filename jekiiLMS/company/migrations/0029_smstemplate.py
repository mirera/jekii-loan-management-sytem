# Generated by Django 4.1 on 2023-07-11 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0028_systemsetting_before_due_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('message', models.TextField()),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.organization')),
            ],
        ),
    ]
