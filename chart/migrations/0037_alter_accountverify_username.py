# Generated by Django 4.1.2 on 2022-12-10 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0036_alter_accountverify_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountverify',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
