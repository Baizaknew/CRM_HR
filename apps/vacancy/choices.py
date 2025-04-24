from django.db.models import TextChoices


class Department(TextChoices):
    MARKETING = 'MKT', 'Маркетинг'
    SALES = 'SLS', 'Продажи'
    FINANCE = 'FIN', 'Финансы'
    IT = 'IT', 'Информационные технологии'
    HR = 'HR', 'Управление персоналом'
    RND = 'RND', 'Исследования и разработка'
    PRODUCTION = 'PRD', 'Производство'
    LOGISTICS = 'LOG', 'Логистика'
    LEGAL = 'LEG', 'Юридический отдел'
    ADMINISTRATION = 'ADM', 'Администрация'
    QUALITY = 'QA', 'Контроль качества'
    SECURITY = 'SEC', 'Безопасность'
    CUSTOMER_SERVICE = 'CS', 'Обслуживание клиентов'


class City(TextChoices):
    BISHKEK = 'BSK', 'Бишкек'
    OSH = 'OSH', 'Ош'
    JALAL_ABAD = 'JBD', 'Джалал-Абад'
    KARAKOL = 'KKL', 'Каракол'
    TOKMOK = 'TKM', 'Токмок'
    NARYN = 'NRN', 'Нарын'
    TALAS = 'TLS', 'Талас'
    BATKEN = 'BTK', 'Баткен'
    BALYKCHY = 'BLC', 'Балыкчы'
    KARA_BALTA = 'KBL', 'Кара-Балта'
    KANT = 'KNT', 'Кант'
    KEMIN = 'KMN', 'Кемин'
    ISFANA = 'ISF', 'Исфана'
    CHOLPON_ATA = 'CPA', 'Чолпон-Ата'
    UZGEN = 'UZG', 'Узген'
    KYZYL_KYA = 'KKY', 'Кызыл-Кия'
    SULUKTU = 'SLK', 'Сулюкта'
    KARA_SUU = 'KSU', 'Кара-Суу'
    AT_BASHI = 'ATB', 'Ат-Баши'
    TOKTOGUL = 'TKT', 'Токтогул'


class Priority(TextChoices):
    HIGHEST = 'P1', 'Срочный'
    HIGH = 'P2', 'Высокий'
    MEDIUM = 'P3', 'Нормальный'
    LOW = 'P4', 'Низкий'
    LOWEST = 'P5', 'Наименьший'


class VacancyRequestStatus(TextChoices):
    IN_REVIEW = 'IN_REVIEW', 'На рассмотрении'
    APPROVED = 'APPROVED', 'Одобрено'
    REJECTED = 'REJECTED', 'Отклонено'