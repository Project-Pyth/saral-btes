# Generated by Django 3.0.6 on 2020-05-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_notification_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalnote',
            name='Subject',
            field=models.CharField(choices=[('Pool Cab', 'PC'), ('Celebrations', 'Cel'), ('Tour', 'Tour'), ('Festival', 'Fest'), ('Others', 'Others')], max_length=30),
        ),
    ]
