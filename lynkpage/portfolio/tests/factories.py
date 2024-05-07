from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from lynkpage.portfolio.models.personal import PersonalCategory
from lynkpage.portfolio.models.personal import PersonalData
from lynkpage.users.tests.factories import UserFactory


# Personal Category Factory for the test
class PersonalCategoryFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = Faker("name")

    class Meta:
        model = PersonalCategory


# Personal Data Factory for the test
class PersonalDataFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    category = SubFactory(PersonalCategoryFactory)
    title = Faker("name")
    link = Faker("url")

    class Meta:
        model = PersonalData
