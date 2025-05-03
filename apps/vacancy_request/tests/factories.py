import factory
from factory.django import DjangoModelFactory

from apps.vacancy.choices import Department, City
from apps.vacancy_request.choices import VacancyRequestStatus
from apps.vacancy_request.models import VacancyRequest
from apps.user.tests.factories import DepartmentHeadFactory


class VacancyRequestFactory(DjangoModelFactory):
    class Meta:
        model = VacancyRequest

    requester = factory.SubFactory(DepartmentHeadFactory)
    approver = None
    department = Department.IT
    city = City.BISHKEK

    title = factory.Sequence(lambda n: f'Vacancy Request #{n}')
    requirements = factory.Faker('paragraph', nb_sentences=3)
    responsibilities = factory.Faker('paragraph', nb_sentences=3)
    rejected_reason = None

    min_salary = factory.Faker('random_int', min=100, max=100000, step=100)
    max_salary = factory.LazyAttribute(lambda vr: vr.min_salary + 500 if vr.min_salary else None)
    approved_at = None

    @factory.post_generation
    def make_approved(self, create, extracted, **kwargs):
        if kwargs.get('is_approved'):
            self.status = VacancyRequestStatus.APPROVED
            self.approver = kwargs.get('approver_user')
            self.approved_at = factory.Faker('past_datetime', start_date='-30d').evaluate(
                None,
                None,
                {'locale': None}
            )

