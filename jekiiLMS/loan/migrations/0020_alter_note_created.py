# Generated by Django 4.1 on 2023-03-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0019_rename_notes_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
