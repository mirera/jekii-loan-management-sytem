# Generated by Django 4.1 on 2023-05-26 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_notification_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='state',
            field=models.CharField(choices=[('warning', 'warning'), ('success', 'success'), ('danger', 'danger'), ('info', 'info'), ('stateless', 'stateless')], default='info', max_length=50),
        ),
    ]
