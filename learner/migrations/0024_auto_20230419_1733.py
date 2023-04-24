# Generated by Django 3.2.18 on 2023-04-19 15:33

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0023_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=ckeditor.fields.RichTextField(),
        ),
    ]