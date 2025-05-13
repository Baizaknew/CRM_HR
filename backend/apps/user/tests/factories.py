import factory

from django.contrib.auth import get_user_model

from factory.django import DjangoModelFactory

from apps.user.choices import UserRole


User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda n: f'{n.username}@gmail.com')
    role = UserRole.RECRUITER
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


    @factory.post_generation
    def set_role(self, create, extracted, **kwargs):
        if extracted:
            self.role = extracted


class DepartmentHeadFactory(UserFactory):
    role = UserRole.DEPARTMENT_HEAD
    username = factory.Sequence(lambda n: f'dh-{n}')


class HrLeadFactory(UserFactory):
    role = UserRole.HR_LEAD
    username = factory.Sequence(lambda n: f'hr-{n}')


class RecruiterFactory(UserFactory):
    role = UserRole.RECRUITER
    username = factory.Sequence(lambda n: f'rc-{n}')
