# Generated by Django 5.0.7 on 2025-04-23 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('DEPARTMENT_LEAD', 'Руководитель'), ('HR_LEAD', 'Глава HR'), ('RECRUITER', 'Рекрутер')], max_length=30, verbose_name='Роль'),
        ),
    ]
