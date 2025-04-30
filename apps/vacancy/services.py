from apps.vacancy.serializers import VacancyCreateSerializer


class VacancyService:
    """Сервис для Вакансий"""
    def create(self, data: dict) -> VacancyCreateSerializer:
        """Создает вакансию"""
        serializer = VacancyCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return serializer
