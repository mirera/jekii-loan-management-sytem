# Generated by Django 4.1 on 2023-04-29 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_alter_organization_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.package'),
        ),
    ]
