# Generated by Django 4.1.5 on 2023-01-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amocrm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='auth_code',
            field=models.CharField(blank=True, max_length=200, verbose_name='App AuthCode'),
        ),
        migrations.AlterField(
            model_name='client',
            name='access_token',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Access token'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.CharField(blank=True, max_length=1000, verbose_name='App Client Secret'),
        ),
        migrations.AlterField(
            model_name='client',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Refresh token'),
        ),
    ]