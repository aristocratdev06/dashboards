# Generated by Django 4.1.2 on 2022-12-05 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0028_accountverify'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountverify',
            name='verfy_account2',
        ),
    ]
