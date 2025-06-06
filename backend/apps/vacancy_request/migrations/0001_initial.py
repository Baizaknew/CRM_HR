# Generated by Django 5.0.7 on 2025-04-29 04:34

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VacancyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('department', models.CharField(choices=[('MKT', 'Маркетинг'), ('SLS', 'Продажи'), ('FIN', 'Финансы'), ('IT', 'Информационные технологии'), ('HR', 'Управление персоналом'), ('RND', 'Исследования и разработка'), ('PRD', 'Производство'), ('LOG', 'Логистика'), ('LEG', 'Юридический отдел'), ('ADM', 'Администрация'), ('QA', 'Контроль качества'), ('SEC', 'Безопасность'), ('CS', 'Обслуживание клиентов')], max_length=50, verbose_name='Отдел')),
                ('city', models.CharField(choices=[('BSK', 'Бишкек'), ('OSH', 'Ош'), ('JBD', 'Джалал-Абад'), ('KKL', 'Каракол'), ('TKM', 'Токмок'), ('NRN', 'Нарын'), ('TLS', 'Талас'), ('BTK', 'Баткен'), ('BLC', 'Балыкчы'), ('KBL', 'Кара-Балта'), ('KNT', 'Кант'), ('KMN', 'Кемин'), ('ISF', 'Исфана'), ('CPA', 'Чолпон-Ата'), ('UZG', 'Узген'), ('KKY', 'Кызыл-Кия'), ('SLK', 'Сулюкта'), ('KSU', 'Кара-Суу'), ('ATB', 'Ат-Баши'), ('TKT', 'Токтогул')], max_length=50, verbose_name='Город')),
                ('requirements', ckeditor.fields.RichTextField(verbose_name='Требования к кандидату')),
                ('responsibilities', ckeditor.fields.RichTextField(verbose_name='Обязанности кандидата')),
                ('rejected_reason', models.CharField(blank=True, max_length=500, null=True, verbose_name='Причина отклонения')),
                ('status', models.CharField(choices=[('IN_REVIEW', 'На рассмотрении'), ('NEEDS_REVISION', 'Требует доработки'), ('APPROVED', 'Одобрено'), ('REJECTED', 'Отклонено')], default='IN_REVIEW', max_length=50, verbose_name='Статус')),
                ('approved_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата согласования HR')),
                ('min_salary', models.IntegerField(blank=True, null=True, verbose_name='Минимальная зарплата')),
                ('max_salary', models.IntegerField(blank=True, null=True, verbose_name='Максимальная зарплата')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vacancy_approvers', to=settings.AUTH_USER_MODEL, verbose_name='Согласующий')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vacancy_requests', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Заявка на подбор',
                'verbose_name_plural': 'Заявки на подбор',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='VacancyRequestComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('vacancy_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='vacancy_request.vacancyrequest', verbose_name='Заявка на подбор')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
