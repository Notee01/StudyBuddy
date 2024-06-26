# Generated by Django 4.2.7 on 2024-03-27 15:19

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_message_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=base.models.Message.image_path, validators=[django.core.validators.FileExtensionValidator(['docx', 'doc'])]),
        ),
        migrations.AlterField(
            model_name='message',
            name='pic',
            field=models.FileField(blank=True, null=True, upload_to=base.models.Message.image_path, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]
