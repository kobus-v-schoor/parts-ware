# Generated by Django 3.1.1 on 2020-09-28 16:12

from django.db import migrations, models
import parts.models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0004_part_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='datasheet',
            field=models.FileField(blank=True, upload_to=parts.models.datasheet_upload_to),
        ),
        migrations.AlterField(
            model_name='part',
            name='image',
            field=models.ImageField(blank=True, upload_to=parts.models.image_upload_to),
        ),
        migrations.AlterField(
            model_name='part',
            name='pinout',
            field=models.ImageField(blank=True, upload_to=parts.models.pinout_upload_to),
        ),
    ]