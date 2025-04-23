from django.contrib import admin

from apps.vacancy.models import Vacancy, VacancyStatus


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status')
    list_filter = ('status', 'department', 'city', 'priority')
    search_fields = ('title',)
    readonly_fields = ('opened_at', 'closed_at', 'time_to_offer')

admin.site.register(VacancyStatus)
