# Generated by Django 3.1.1 on 2020-09-28 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0002_auto_20200928_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='slug',
        ),
    ]
