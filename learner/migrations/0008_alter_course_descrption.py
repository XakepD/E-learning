# Generated by Django 3.2.18 on 2023-03-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0007_auto_20230324_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='descrption',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
