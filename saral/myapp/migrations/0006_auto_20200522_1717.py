# Generated by Django 3.0.6 on 2020-05-22 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200522_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalnote',
            old_name='Subject',
            new_name='Sub',
        ),
    ]
