# Generated by Django 4.1 on 2023-04-01 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_no', models.CharField(max_length=10, unique=True)),
                ('logo', models.ImageField(default='default.png', upload_to='profile_photos/')),
                ('favicon', models.ImageField(default='default.png', upload_to='profile_photos/')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('address', models.CharField(max_length=100)),
                ('site_title', models.CharField(max_length=100)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
