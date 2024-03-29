# Generated by Django 4.1 on 2023-03-28 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0024_alter_member_passport_photo'),
        ('loan', '0029_alter_loan_attachments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('loan_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_as_no', to='loan.loan')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.member')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
