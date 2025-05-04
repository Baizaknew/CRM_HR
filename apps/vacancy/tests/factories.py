import factory

from factory.django import DjangoModelFactory

from apps.user.tests.factories import DepartmentHeadFactory, RecruiterFactory
from apps.vacancy.choices import Department, City, Priority
from apps.vacancy.models import Vacancy, VacancyStatus
from apps.vacancy_request.tests.factories import VacancyRequestFactory


class VacancyStatusFactory(DjangoModelFactory):
    class Meta:
        model = VacancyStatus
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Status-{n}')
    is_default = False
    is_opened = False
    is_closed = False


class VacancyFactory(DjangoModelFactory):
    class Meta:
        model = Vacancy

    title = factory.Sequence(lambda n: f"Vacancy {n}")
    department = Department.IT
    city = City.BISHKEK
    requirements = factory.Faker('paragraph', nb_sentences=3)
    responsibilities = factory.Faker('paragraph', nb_sentences=3)

    priority = Priority.MEDIUM
    status = factory.SubFactory(VacancyStatusFactory)
    department_lead = factory.LazyAttribute(lambda o: o.vacancy_request.requester)
    recruiter = None
    salary = factory.Faker('sentence', nb_words=4)
    vacancy_request = factory.SubFactory(VacancyRequestFactory)
    opened_at = None
    closed_at = None
    time_to_offer = None
