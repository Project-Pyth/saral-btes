# Generated by Django 3.0.6 on 2020-05-23 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20200522_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='designation',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Employee', 'Employee')], max_length=15),
        ),
    ]
