# Generated by Django 5.0.7 on 2025-05-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy_request', '0003_alter_vacancyrequestcomment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancyrequestchangehistory',
            name='new_status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Новый статус'),
        ),
        migrations.AlterField(
            model_name='vacancyrequestchangehistory',
            name='old_status',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Старый статус'),
        ),
    ]
