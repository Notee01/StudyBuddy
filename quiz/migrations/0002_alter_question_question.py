# Generated by Django 4.2.7 on 2024-04-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
