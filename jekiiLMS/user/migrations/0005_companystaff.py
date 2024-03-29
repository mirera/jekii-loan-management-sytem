# Generated by Django 4.1 on 2023-04-04 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0014_alter_branch_company'),
        ('user', '0004_remove_superadmin_date_joined_branchmanager_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(choices=[('admin', 'ADMIN'), ('staff', 'STAFF')], max_length=10)),
                ('staff_role', models.CharField(choices=[('general staff', 'G.STAFF')], max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('id_no', models.CharField(max_length=10, unique=True)),
                ('phone_no', models.CharField(max_length=10, unique=True)),
                ('profile_photo', models.ImageField(default='default.png', upload_to='profile_photos/')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('branch', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='branch.branch')),
            ],
        ),
    ]
