# Generated by Django 3.1.1 on 2020-09-28 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0003_remove_part_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
