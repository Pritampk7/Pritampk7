# Generated by Django 3.1.7 on 2021-04-08 13:18

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
            name='post_data',
            fields=[
                ('id', models.CharField(default='', max_length=70, primary_key=True, serialize=False)),
                ('data', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP_address', models.GenericIPAddressField(default='', null=True)),
                ('username', models.CharField(default='', max_length=15)),
                ('password', models.CharField(default='', max_length=20)),
                ('device_type', models.CharField(default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='hostname',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.ForeignKey(default='', max_length=15, on_delete=django.db.models.deletion.CASCADE, to='users.user_data')),
            ],
        ),
    ]
