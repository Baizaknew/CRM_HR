# Generated by Django 5.0.7 on 2025-05-05 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_candidatenote_added_by_candidatereference_added_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidateapplicationstatus',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name='Статус по умолчанию'),
        ),
    ]
