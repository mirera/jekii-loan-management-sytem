# Generated by Django 4.1 on 2023-05-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_alter_mpesasetting_shortcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailsetting',
            name='app_consumer_secret',
        ),
        migrations.AddField(
            model_name='emailsetting',
            name='smpt_port',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
