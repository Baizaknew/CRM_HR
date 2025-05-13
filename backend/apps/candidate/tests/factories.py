from apps.candidate.choices import Experience, SourceType
from apps.candidate.models import Candidate, CandidateNote, CandidateReference, CandidateSource, CandidateTag, CandidateApplication, CandidateApplicationStatus
from apps.user.tests.factories import UserFactory
from apps.vacancy.tests.factories import VacancyFactory
CandidateReference, CandidateNote, CandidateSource
import factory
from apps.vacancy.choices import Department, City, Priority


from factory.django import DjangoModelFactory


class CandidateTagFactory(DjangoModelFactory):
    class Meta:
        model = CandidateTag
        django_get_or_create = ('title',)

    title = factory.Sequence(lambda n: f'Тег {n}')


class CandidateSourceFactory(DjangoModelFactory):
    class Meta:
        model = CandidateSource
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Источник {n}')



class CandidateApplicationStatusFactory(DjangoModelFactory):
    class Meta:
        model = CandidateApplicationStatus
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'Статус заявки {n}')
    order = factory.Sequence(lambda n: n)
    is_rejected = False
    is_success = False
    is_default = False



class CandidateNoteFactory(DjangoModelFactory):
    class Meta:
        model = CandidateNote

    text = factory.Faker('paragraph', nb_sentences=2)
    candidate = factory.SubFactory("apps.candidate.tests.factories.CandidateFactory")
    added_by = factory.SubFactory(UserFactory)


class CandidateReferenceFactory(DjangoModelFactory):
    class Meta:
        model = CandidateReference

    text = factory.Faker('paragraph', nb_sentences=3)
    candidate = factory.SubFactory("apps.candidate.tests.factories.CandidateFactory")
    added_by = factory.SubFactory(UserFactory)


class CandidateFactory(DjangoModelFactory):
    class Meta:
        model = Candidate

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    patronymic = factory.Faker('middle_name_male', locale='ru_RU')
    resume = None

    city = factory.Iterator(City.choices, getter=lambda c: c[0])
    experience = factory.Iterator(Experience.choices, getter=lambda c: c[0])
    phone_number = factory.Faker('phone_number', locale='ru_RU')
    email = factory.Sequence(lambda n: f'candidate{n}@example.com')
    cover_letter = factory.Faker('paragraph', nb_sentences=5)

    salary_expectation = factory.LazyFunction(lambda: f"{factory.Faker('random_int', min=50, max=200).evaluate(None,None,{})}000")
    source = factory.SubFactory(CandidateSourceFactory)
    source_type = SourceType.APPLICATION
    added_by = factory.SubFactory(UserFactory)


class CandidateApplicationFactory(DjangoModelFactory):
    class Meta:
        model = CandidateApplication
        django_get_or_create = ('candidate', 'vacancy')

    candidate = factory.SubFactory(CandidateFactory)
    vacancy = factory.SubFactory(VacancyFactory)
    status = factory.SubFactory(CandidateApplicationStatusFactory)
    recruiter = factory.SubFactory(UserFactory, role='recruiter')

    rejected_reason = factory.Maybe(
        'status__is_rejected',
        yes_declaration=factory.Faker('sentence', nb_words=5),
        no_declaration=None,
    )
